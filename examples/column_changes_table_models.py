#
# Major use case for this functionality is pivoted tables/views of "Custom Fields"
# Often stored originally in "long" attribute->value tables, they should be pivoted into
# Column Per Attribute for reporting and analysis
# By their nature, each table/view will have different columns and the Table + Model objects
# must be generated programmatically before being imported via TML Import REST API

from copy import deepcopy

from thoughtspot_tml import *
from thoughtspot_tml.utils import *
# _scriptablity holds the EDoc classes for complex data structures
from thoughtspot_tml._scriptability import *

# Python request library for HTTP calls
from requests import *

# REST API library installable via pip
from thoughtspot_rest_api_v1 import *

# Please see documentation at https://github.com/thoughtspot/thoughtspot_rest_api_v1_python
# for all the ways to initialize and auth with library
ts_url = "https://{}.thoughtspot.cloud"
dev_org_id = 102832
# Here we assume you have valid bearer token for user somehow, replace with any other auth pattern
dev_org_bearer_token = "{}"
ts = TSRestApiV2(server_url=ts_url)
ts.bearer_token = dev_org_bearer_token

ts_dest_org_bearer_token = {}

# This just shows the basic way that the column_id property in a Model
# is constructed to reference to a column in a Table object
def generate_column_id_reference_for_model(table: Table):
    table_alias = table.table.name
    cols = table.table.columns
    for col in cols:
        table_col_id = "{}::{}".format(table_alias, col.name)
    return cols

# Returns a fully constructed new Table Column that can be appended to Table.table.columns
def get_table_column():
    t_col = LogicalTableEDocProtoLogicalColumnEDocProto()
    t_col.properties = ColumnProperties()
    t_col.db_column_properties = LogicalTableEDocProtoDbColumnProperties()
    return t_col

# Returns a fully constructed new Model Column that can be appended to Model.model.columns
def get_model_column():
    m_col = WorksheetEDocProtoWorksheetColumn()
    m_col.properties = ColumnProperties()
    return m_col

def get_ws_column():
    return get_model_column()

# Given a Table tml object, get the equivalent Model columns with proper column_id
def generate_model_columns_from_table(table: Table):
    m_cols = []
    table_alias = table.table.name
    cols = table.table.columns
    for col in cols:
        m_col = get_model_column()

        table_col_id = "{}::{}".format(table_alias, col.name)
        # print(ref)

        # Fill in the Model column details with same settings from Table column
        m_col.name = col.name
        m_col.column_id = table_col_id
        m_col.properties.column_type = col.properties.column_type
        m_col.properties.index_type = col.properties.index_type
        if m_col.properties.aggregation is not None:
            m_col.properties.aggregation = col.properties.aggregation
        m_cols.append(m_col)

    return m_cols

# Append model columns from generate_model_columns_from_table, with logic for
# updating / handling duplicates
#  - Cannot have two fields with the same name (case-insensitive)
#  - Cannot have two fields with reference to the same Column from one a Table?
def append_model_columns(model: Model, new_model_cols, replace_if_exists=False):
    cur_mod_cols = deepcopy(model.model.columns)
    # Check for duplicates - name, column_id, both?

    for col in new_model_cols:
        cur_mod_cols.append(col)

    return cur_mod_cols

#
# Assumes array with following properties for each column
# You can determine how to get these (and any other properties, but these are standard
# Also assume the Model Column has the same name as the Table column
# { 'name' : , 'db_column_name': , 'data_type': , 'column_type' : , 'index_type': }
# There are no protections in this function against duplicates / etc. - assumes you have
# Only the set of columns to be added, while the Table and Model already have the 'non-variable columns'
#
def add_cols_to_table_and_model(table: Table, model: Model, col_definitions: List):
    t_cols = table.table.columns
    m_cols = model.model.columns

    for col in col_definitions:
        new_t_col = get_table_column()
        new_m_col = get_model_column()

        new_t_col.name = col['name']
        new_m_col.name = col['name']

        new_m_col.column_id = "{}::{}".format(table.table.name, col['name'])

        new_t_col.db_column_name = col['db_column_name']
        new_t_col.db_column_properties.data_type = col['data_type']

        new_t_col.properties.column_type = col['column_type']
        new_t_col.properties.index_type = col['index_type']
        if new_t_col.properties.aggregation is not None:
            new_t_col.properties.aggregation = col['aggregation']

        new_m_col.properties.column_type = col['column_type']
        new_m_col.properties.index_type = col['index_type']
        if new_m_col.properties.aggregation is not None:
            new_m_col.properties.aggregation = col['aggregation']

        t_cols.append(new_t_col)
        m_cols.append(new_m_col)

#
# The ideal setup will have the same ThoughtSpot Table name for the Custom Fields table
# (the db_table_name can be different for each object)
# However in a dev environment, you may find the need for different ThoughtSpot Table names
# To handle this, you'll need to adjust the model_tables: and joins: section within
# Example of a Model TML with one table and one join:
#
#   model_tables:
#   - name: FACT_SALES
#     joins:
#     - with: CUSTOM_FIELDS_A
#       'on': '[FACT_SALES::PRODUCTID] = [CUSTOM_FIELDS_A::PRODUCTID]'
#       type: INNER
#       cardinality: MANY_TO_ONE
#     obj_id: SNOW_DEV__FACT_SALES
#   - name: CUSTOM_FIELDS_A
#     obj_id: SNOW_DEV__CUSTOM_FIELDS_A
#
# You can't do a pure FIND/REPLACE because it might affect obj_id

def replace_table_name_in_model(model: Model, old_table_name, new_table_name, new_table_obj_id=None):
    for table in model.model.model_tables:
        # Swap out the table reference
        if table.name == old_table_name:
            table.name = new_table_name
            if new_table_obj_id is not None:
                table.obj_id = new_table_obj_id
        # Swap out any JOIN references
        if table.joins is not None:
            for j in table.joins:
                if j.with_ == old_table_name:
                    j.with_ = new_table_name
                    j.on = j.on.replace(old_table_name, new_table_name)


# This example presumes you have set obj_id (available in 10.6) for all the objects in your Dev Org
# See https://github.com/thoughtspot/thoughtspot_rest_api_v1_python/blob/main/examples_v2/set_obj_id.py
# obj_id is unique Per Org, and thus can be used as an consistent identifier BETWEEN Orgs

# This function is copied from set_obj_id.py

def export_tml_with_obj_id(ts: TSRestApiV2, guid:Optional[str] = None,
                           obj_id: Optional[str] = None,
                           save_to_disk=True):
    # Example of metadata search using obj_identifier (the property may be updated?)
    if obj_id is not None:
        search_req = {
            "metadata": (
                {'obj_identifier': obj_id}
            ),
            "sort_options": {
                "field_name": "CREATED",
                "order": "DESC"
            }
        }

        tables = ts.metadata_search(request=search_req)
        if len(tables) == 1:
            guid = tables[0]['metadata_id']
            obj_id = tables[0]['metadata_header']['objId']

        # print(json.dumps(log_tables, indent=2))

    if guid is None:
        raise Exception()

    # export_options allow shifting TML export to obj_id, without any guid references
    exp_opt = {
        "include_obj_id_ref": True,
        "include_guid": False,
        "include_obj_id": True
    }


    yaml_tml = ts.metadata_tml_export(metadata_ids=[guid], edoc_format='YAML',
                                      export_options=exp_opt)

    # Get obj_id from the TML
    lines = yaml_tml[0]['edoc'].splitlines()
    if obj_id is None:
        if lines[0].find('obj_id: ') != -1:
            obj_id = lines[0].replace('obj_id: ', "")

    obj_type = lines[1].replace(":", "")

    if save_to_disk is True:
        print(yaml_tml[0]['edoc'])
        print("-------")

        # Save the file with {obj_id}.{type}.{tml}
        filename = "{}.{}.tml".format(obj_id, obj_type)
        with open(file=filename, mode='w') as f:
            f.write(yaml_tml[0]['edoc'])

    return yaml_tml

#
# Overall pattern and steps within ThoughtSpot prior what this script shows doing
#

# 1. Start with the full data object set, including one template "Custom Fields Table", in your dev org, via the ThoughtSpot UI
# 1.5 Set obj_id for each item using Update Metadata Header (in 10.6) or Update Metadata Obj Id (in 10.8) REST APIs
#	- this includes the Connection (you may want the Connection Name to be the same in every Org as well, but obj_id is a separate property)
#
# 2. Remove all Columns from the Custom Fields Table in the Model down to just the Join Key + Other Common Fields
# 	- Change the JOIN type of the Custom Fields Table in the Model to be a "local JOIN", so that it will be fully defined by the Model TML file rather than referencing a JOIN defined in a Table file.
# 	- This is especially important if the Custom Fields Table is going to have a different name in ThoughtSpot in each Org.
# 3. Reduce the Custom Fields Table down to just the Join Key field (and any others that will be common to each Custom Fields Table)

#
# WE START HERE:
#
# 4. Export the entire data model using the TML Export API set to export with obj_id rather than GUID

model_guid = ""
custom_fields_table_guid = ""
table_guids = []  # All tables that won't be modified


# Model obj, then Custom Fields Table
try:
    model_resp = export_tml_with_obj_id(ts=ts, guid=model_guid, save_to_disk=False)
    # The 'edoc' property is the actual YAML string to be loaded
    model_obj = Model.loads(model_resp[0]['edoc'])
except requests.exceptions.HTTPError as e:
    print(e)
    print(e.response.content)
    exit()

try:
    cust_fields_resp = export_tml_with_obj_id(ts=ts, guid=custom_fields_table_guid, save_to_disk=False)
    # The 'edoc' property is the actual YAML string to be loaded
    cust_fields_obj = Table.loads(cust_fields_resp[0]['edoc'])
except requests.exceptions.HTTPError as e:
    print(e)
    print(e.response.content)
    exit()


# 5. Get the details about the Custom Fields you need to add to the Custom Fields Table and the Model
# format for columns: [ { 'name' : , 'db_column_name': , 'data_type': , 'column_type' : , 'index_type': }]

def get_custom_columns():
    # You may use any number of techniques to programmatically retrieve these column names and attributes
    # Remember to leave out anything you left in the Table and Model, just the fields that vary

    # This is just a hardcoded return to show you the format for the minimal details to return
    custom_columns = [
        {"name": "Product Name", "db_column_name": "PRODUCTNAME", "data_type": "VARCHAR",
         "column_type": "ATTRIBUTE", "index_type": "DONT_INDEX"},
        {"name": "Unit Retail Price", "db_column_name": "UNIT_PRICE", "data_type": "INT64",
         "column_type": "MEASURE", "index_type": "DONT_INDEX", "aggregation": "AVG"},
    ]
    return custom_columns

# If you need to replace the Table Name, change in Table Obj and the Model
old_t_name = 'CUSTOM_FIELDS_DEV'
new_t_name = 'CUSTOM_FIELDS'
new_table_obj_id = 'Connection_Name__CUSTOM_FIELDS'

cust_fields_obj.table.name = new_t_name
replace_table_name_in_model(model=model_obj, old_table_name=old_t_name, new_table_name=new_t_name,
                            new_table_obj_id=new_table_obj_id)

# Add the columns to both Table and Model
add_cols_to_table_and_model(table=cust_fields_obj, model=model_obj, col_definitions=get_custom_columns())

# Get set of TML strings ready to import

cust_fields_yaml = cust_fields_obj.dumps(format_type='YAML')
model_yaml = model_obj.dumps(format_type='YAML')

all_tml_to_import = [cust_fields_yaml, model_yaml]

# All other tables
for t_guid in table_guids:
    try:
        model_resp = export_tml_with_obj_id(ts=ts, guid=t_guid, save_to_disk=False)
        # The 'edoc' property is the actual YAML string to be loaded
        all_tml_to_import.append(model_resp[0]['edoc'])
    except requests.exceptions.HTTPError as e:
        print(e)
        print(e.response.content)
        exit()

# Change to the destination Org by switching bearer token
ts.bearer_token = ts_dest_org_bearer_token

# See http://github.com/thoughtspot/thoughtspot_rest_api_v1_python/blob/main/examples_v2/publish_tml.py for more
try:
    tml_import_resp = ts.metadata_tml_import(metadata_tmls=all_tml_to_import, import_policy='PARTIAL', create_new=False)
except requests.exceptions.HTTPError as e:
    print(e)
    print(e.response.content)
    exit()
