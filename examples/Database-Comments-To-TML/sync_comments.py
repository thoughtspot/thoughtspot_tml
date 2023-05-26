from thoughtspot_tml.utils import determine_tml_type
from thoughtspot_tml import Table
from thoughtspot_rest_api_v1 import *
import csv
from typing import List
from thoughtspot_tml import _scriptability
import requests

# Connection GUID
connection_guid = '5924acaf-7ac0-4128-a5c7-4c18b7230617'

# Or name
connection_name = 'databricks'

# Databricks source
db_name = "hive_metastore"
schema = 'dev'
db_table = "dl_dataset_facebook"

username = 'your thoughtspot user'  
password = 'your password'
server = 'https://yourCluster.cloud/'     

# ThoughtSpot class wraps the V1 REST API
ts: TSRestApiV1 = TSRestApiV1(server_url=server)
try:
    ts.session_login(username=username, password=password)
except requests.exceptions.HTTPError as e:
    print(e)
    print(e.response.content)
    
tml_cls = determine_tml_type(path='TEMPLATE.table.tml')
tml = tml_cls.load(path='TEMPLATE.table.tml')      
    
#build the top section of the tml file
tml.guid =  None
tml.table.name =db_table
tml.table.db=db_name
tml.table.schema=schema
tml.table.db_table=db_table
tml.table.connection.name=connection_name

tml.table.joins_with = None # setting this so we can avoid a relationship warning

#function for reading in the csv and setting the properties, creating columns
def create_tml_table_columns_input_file(filename: str) -> List[_scriptability.LogicalTableEDocProtoLogicalColumnEDocProto]:
    """Create ThoughtSpot table object columns from a CSV file."""
    thoughtspot_data_converter = {
        "bigint": "INT64",
        "string": "VARCHAR",
    }
    columns = []

    with open(filename) as c:
        reader = csv.DictReader(c, delimiter=',', quotechar='"')

        for row in reader:
            ts_data_type = thoughtspot_data_converter.get(row["data_type"], "VARCHAR")
            
            if ts_data_type == "INT64":
                ts_column_type = "MEASURE"
            else:
                ts_column_type = "ATTRIBUTE"
            
            column = _scriptability.LogicalTableEDocProtoLogicalColumnEDocProto(
                name=row["col_name"],
                description=row["col_desc"],
                db_column_name=row["db_column_name"],
                properties={"index_type": row["index_type"],"column_type": ts_column_type },
                db_column_properties={"data_type": ts_data_type}
            )

            columns.append(column)
         
    return columns

if __name__ == "__main__":
    table_csv_input_filename = "column_input.csv"
    columns = create_tml_table_columns_input_file(table_csv_input_filename)

# add the new columns to the table tml
tml.table.columns=columns

# Write to disk, if using the UI to publish
tml.dump(f'databricks.{tml.tml_type_name}.tml') #name.type.tml

# If using the API to publish:
ts.metadata_tml_import(tml.dumps(format_type="YAML"), create_new_on_server=True, validate_only=False)
