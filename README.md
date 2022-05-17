# thoughtspot_tml
Python library for working with ThoughtSpot Modeling Language (TML) files programmatically

## ThoughtSpot Modeling Language
ThoughtSpot Modeling Language (TML) is a YAML based representation of objects in ThoughtSpot. The TML format for each object type is documente at https://cloud-docs.thoughtspot.com/admin/ts-cloud/tml.html . 

The ThoughtSpot REST API can export and import TML in JSON as well as YAML. The user interface to ThoughtSpot only shows the YAML based format, so we recommend using YAML when saving to disk.

## thoughtspot_tml overview
The thoughtspot_tml library provides classes modeling the TML representation of each ThoughtSpot object type (Tables, Worksheets, Views, Answers, Liveboards).

There is also a helper class called `YAMLTML` for processing files in TML YAML format.

Each of the TML classes takes an input of an OrderedDict in the constructor, which becomes the `.tml` property of the objects.

Methods then exist in each class to manipulate the specific properties of the various types.

## REST API import and export of TML to work with thoughtspot_tml
The constructor of each TML object class requires an OrderedDict Python object.

thoughtspot_tml does not handle the REST API calls to import and export TML from a ThoughtSpot instance.

Any library wishing to use the thoughtspot_tml objects should output an OrderedDict from the TML export API, and accept an OrderedDict in the import command (then convert to JSON or YAML).

Alternatively, a library can export the YAML string from the REST API, then use the YAMLTML class to load into an OrderedDict, and use the YAMLTML class to dump to YAML string for import.

## GUIDs 
TML files downloaded from a ThoughtSpot instance will have a `guid` property at the top of the file. 

GUID is the unique identifier within the given ThoughtSpot instance. 

When you import a TML file, if the `guid` property in the TML file matches to an existing object on a ThoughtSpot instance, the existing object will be updated.

If there is no `guid` property in the file or there is no match to an existing guid, a new object is created with a *new GUID*. 

The REST API import call has an argument that *forces new objects to be created, even if they contain a guid property*.

In any case where a new object is created, the TML file you import will not be exactly what exists on the ThoughtSpot instance, because the new GUID will be added at the top of the TML file when you export it again.

## Installing thoughtspot_tml
You should be able to install thoughtspot_tml via pip:

    pip install thoughtspot_tml

## Using thoughtspot_tml
The simplest way to use thoughtspot_tml is:

    from thoughtspot_tml import *

This will get you the YAMLTML helper class as well as each of the ThoughtSpot object classes: Table, Worksheet, View, Answer, Liveboard

### Retrieving the TML as a Python OrderedDict from REST API
As noted above, each TML object uses an OrderedDict. If a library returns the OrderedDict, you can load that directly into the object constructor: 

The following example shows using a library where the `export_tml(guid)` method returns an OrderedDict. 

    lb_od = ts.tml.export_tml(guid=lb_guid)
    # Create a Liveboard TML object
    lb_obj = Liveboard(lb_od)
    # Or do it all in one step: 
    lb_obj = Liveboard(ts.tml.export_tml(guid=lb_guid))

#### Retrieving TML with associated object GUIDs
At the current time, TML export does not include the GUIDs of "table objects" (really data objects), only their names.

When doing SDLC processes, it is very useful to store the exact GUIDs for these objects in the TML file initially. 

The GUIDS of the associated objects can be retrieved from the REST API call that requests the TML, by using the 'export_associated=true' argument in the REST API call to `/metadata/tml/export`.

The `Worksheet`, `View`, `Answer` and `Liveboard` classes all have a method called `add_fqns_from_name_guid_map(name_guid_map)` which takes in a dict in form `{ 'name' : 'guid' }`. This will add the GUID as the additional 'FQN' property within the `table` section of the file. `Table` objects do not need this method, because Connections have unique names, so Connection Name or other connection details can be changed directly.

The following example uses the thoughtspot-rest-api-v1 module, where `metadata_export_tml_with_associations_map` returns both the OrderedDict of the main exported TML object and a `{'name': 'guid'}` Dict generated from all the other associated objects that can be used in the `.add_fqns_from_name_guid_map()` method

    lb_od, name_guid_map = ts.tsrest.metadata_export_tml_with_associations_map(guid=lb_guid)
    # Create a Liveboard TML object
    lb_obj = Liveboard(lb_od)
    lb_obj.add_fqns_from_name_guid_map(name_guid_map=name_guid_map)
    

### Retrieving TML as YAML string from REST API
If the REST API library outputs the YAML string from the TML export call, you can use the YAMLTML class to load it to OrderedDict:

    lb_yaml = ts.tml.export_tml_string(guid=lb_guid)
    lb_od = YAMLTML.load_string(lb_yaml)

    # Create a Liveboard TML object
    lb_obj = Liveboard(lb_od)
    # Or do it all in one step: 
    lb_obj = Liveboard(YAMLTML.load_string(ts.tml.export_tml_string(guid=lb_guid)))

#### Retrieving TML with associated object GUIDs
At the current time, TML export does not include the GUIDs of "table objects" (really data objects), only their names.

When doing SDLC processes, it is very useful to store the exact GUIDs for these objects in the TML file initially. 

The GUIDS of the associated objects can be retrieved from the REST API call that requests the TML, by using the 'export_associated=true' argument in the REST API call to `/metadata/tml/export`.

The `Worksheet`, `View`, `Answer` and `Liveboard` classes all have a method called `add_fqns_from_name_guid_map(name_guid_map)` which takes in a dict in form `{ 'name' : 'guid' }`. This will add the GUID as the additional 'FQN' property within the `table` section of the file. `Table` objects do not need this method, because Connections have unique names, so Connection Name or other connection details can be changed directly.

The following example uses the thoughtspot-rest-api-v1 module, where library where `metadata_export_tml_with_associations_map` returns both the string representation of the main exported TML object and a `{'name': 'guid'}` Dict generated from all the other associated objects that can be used in the `.add_fqns_from_name_guid_map()` method:

    lb_str, name_guid_map = ts.tsrest.metadata_export_tml_string_with_associations_map(guid=lb_guid)
    # Create a Liveboard TML object
    lb_obj = Liveboard(YAMLTML.load_string(lb_str))
    lb_obj.add_fqns_from_name_guid_map(name_guid_map=name_guid_map)
    final_yaml_str = YAMLTML.dump_tml_object(lb_obj)
    with open('tml_file.liveboard.tml', 'w', encoding='utf-8') as fh:
        fh.write(final_yaml_str)

### Opening a TML file from disk and loading into a TML object
The `YAMLTML` object contains static methods to help with correct import and formatting of ThoughtSpot's TML YAML.

    with open('tml_file.worksheet.tml', 'r', encoding='utf-8') as fh:
        tml_yaml_str = fh.read()

    tml_yaml_ordereddict = YAMLTML.load_string(tml_yaml_str)

    tml_obj = Worksheet(tml_yaml_ordereddict)

    tml_obj.description = "Adding a wonderful description to this document"


Full example of working with a YAML string in `examples/tml_yaml_intro.py`.

### Factory method for getting objects
`YAMLTML.get_tml_object(tml_yaml_str)` returns back the appropriate object for the type of TML object opened. 

You can then check the `.content_type` property before attempting actions that are specific to a given object type.

Remember that the TML content_type property for a Liveboard is still `pinboard` at this time.

    with open('tml_file.worksheet.tml', 'r', encoding='utf-8') as fh:
        tml_yaml_str = fh.read()

    tml_obj = YAMLTML.get_tml_object(tml_yaml_str)

    tml_obj.description = tml_obj.description + "(Copied from previous instance)"
    if tml_obj.content_type == 'pinboard':
        # Liveboard specific changes

### Dumping to YAML or JSON
Each TML object keeps the OrderedDict representing the TML file itself in the `.tml` property.

To export to a YAML string that matches the ThoughtSpot format exactly, use `YAMLTML.dump_tml_object(tml_object)`. 

To export to a JSON string (if necessary), use the standard Python json library to dump the `TMLObject.tml` property: `json.dumps(tml_object.tml, indent=2)`

Note that `YAMLTML.dump_tml_object()` takes the full TML object, vs. passing the `.tml` property using `json.dumps()`

    tml_obj = Worksheet(tml_yaml_ordereddict)

    tml_obj.description = "Adding a wonderful description to this document"
    modified_tml_string = YAMLTML.dump_tml_object(tml_obj)
    with open('modified_tml.worksheet.tml', 'w', encoding='utf-8') as fh:
        fh.write(modified_tml_string)

### TML base class
You can create a base TML object, which only has the .content and .content_name properties

    tml_obj = TML(tml)
    tml_obj.content["additional_keys"]["sub-keys"]

But if you know the type of object, then you can use one of the descendant objects to give
more built in properties to access rather than having to work through the .content property.

Remember: make sure you are referencing the property from `TML.content['{key_1}']['{key_2}]` when you are setting changes - if you have made and modified a variable from the original values, it may not be part of the `.content` dictionary unless you fully qualify.

### Table class
Table objects are the fundamental component of data models in ThoughtSpot, representing the actual table-like objects on a data source (tables, views, etc.)

Table objects also hold the Row Level Security rules in ThoughtSpot.

#### Modifying Connection details
Connections in ThoughtSpot all have unique names, so to switch a Table to a different connection, use the `Table.connection_name` property

    table_obj.connection_name = 'New Connection Name'

The `Table.change_connection_by_name(original_connection_name: str, new_connection_name: str)` method exists as well to safely change the name only if the original connection name matches the provided value. This allows for safe find/replace over a number of files / objects.

The other properties are available to modify as well:

 - db_name
 - schema
 - db_table

#### Table Columns
To access existing columns as a List, use the `Table.columns` property

To add a column, first use `Table.create_column()` to retrieve a column object, then use `Table.add_column()` to add the column to the end of the existing list. `Table.add_columns()` takes a List of columns to add many at once.

    new_column = table_obj.create_column(column_display_name='Pretty Name', db_column_name='db_name_of_col', column_data_type='INT64'
                      column_type='ATTRIBUTE', index_type='DONT_INDEX')
    table_obj.add_column(new_column)


See the reference guide https://docs.thoughtspot.com/cloud/latest/tml#syntax-tables for string values of these properties.


#### Creating a Table TML programmatically
The Table class has a static method called `generate_tml_from_scratch(connection_name: str, db_name: str, schema: str, db_table: str)` which returns a str in YAML format with the start of a Table TML and no columns.

The string template can then be loaded into a Table constructor using `YAMLTML.load_string()` to give a blank

    tml_yaml_str = Table.generate_tml_from_scratch(connection_name='Main Snowflake Connection', db_name="IMPORTANT_DATABASE,
                                                   schema='PUBLIC', db_table='MY_TABLE')
    tml_obj = Table(YAMLTML.load_string(tml_yaml_str)

You can then create new columns and add them to this basic "empty" Table object. The necessary properties could come from an input file or via REST API details from ThoughtSpot or a data catalog.

Example of a function to read in column definitions from a file:

    # 'CSV' format for a table is
    # db_column_name|column_name|data_type|attribute_or_measure|index_type
    def create_tml_table_columns_input_file(filename):
        new_columns = []
        with open(filename, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter='|', quotechar='"')
    
            row_count = 0
            for row in csvreader:
                # skip header
                if row_count == 0:
                    row_count = 1
                    continue
                db_col_name = row[0]
                col_name = row[1]
                col_data_type = row[2]
                col_type = row[3]
                index_type = row[4]
                # Simple algorithm for making numeric columns MEASURE by default
                if col_data_type in ['DOUBLE', 'INT64']:
                    col_type = 'MEASURE'
                new_column = table_obj.create_column(column_display_name=col_name,
                                                     db_column_name=db_col_name,
                                                     column_data_type=col_data_type, column_type=col_type,
                                                     index_type=index_type)
                new_columns.append(new_column)
        return new_columns

### Worksheet class
Worksheets are the data model layer presented to end users. They present a single controlled source from multiple tables with many additional controls on how columns are displayed and indexed.

#### Changing Table references in a Worksheet
Tables, unlike Connections, do not have fully unique names in ThoughtSpot. If there is more than one Table with the same name, you will need to use the GUID of the table to identify it. 

The property in TML for a GUID reference is `fqn:` . 

Worksheet class provides the `remap_tables_to_new_fqn(name_to_fqn_map: Dict)` method to perform a GUID swap. You create a Dict of { 'name' : 'fqn' } structure, then pass it in and the correct TML manipulations will happen calling the `change_table_by_fqn()` method.

    name_guid_map = { 'Table 1' : '0f814ce1-dba1-496a-b3de-38c4b9a288ed', 'Table 2' : '2e7a0676-2acf-4700-965c-efebf8c0b594'}
    ws_obj.remap_table_to_new_fqn(name_to_fqn_map=name_guid_map)

#### Creating a Worksheet programmatically from a Table TML
If you want to make a worksheet on top of a single table, you can generate the Worksheet programmatically from that Table TML

The Worksheet class has a static method called `generate_tml_from_scratch(worksheet_name: str, table_name: str)` which returns a str in YAML format with the start of a Worksheet TML and no columns.

The string template can then be loaded into a Worksheet constructor using `YAMLTML.load_string()` to give a blank

    tml_yaml_str = Worksheet.generate_tml_from_scratch(worksheet_name='Great Worksheet', table_name=table_tml_obj.content_name)
    tml_obj = Worksheet(YAMLTML.load_string(tml_yaml_str)

A full example of creating a Worksheet TML programmatically is available in examples/tml_and_sdlc/tml_from_scratch.py.

#### Worksheet Columns

### Liveboard class
A Liveboard is a combination of Answers, but each Answer lives fully within the TML of the Liveboard (that is to say, Answers on a Liveboard live in the Liveboard object fully, they are not links to Answer objects stored independently in ThoughtSpot).

The TML for an Answer within a Liveboard is almost identical to the TML for separately stored Answer. The Liveboard class has a special `.answers_as_objects` property that returns a list of Answer objects automatically.

    pb_obj = Liveboard(ts.export_tml(guid=pb_guid))
    answers = pb_obj.answers_as_objects  # Returns list of Answer objects from Liveboard
    for a in answers:
        print(a.search_query)

#### Changing the Order or Size of Answers
Liveboards have an `answers` section that defines each answer, and then a `layout` section that defines the order and sizing of the answers. 

The 'tiles' section of the Layout is an ordered list / array. The order the elements appear in the tiles list is the order they will appear in the Liveboard, then space optimized based on the sizes that have been chosen.

There is an enum `Liveboard.TileSizes` to use to get the strings for the layout sizes.

To change the order or sizing, access the `Liveboard.layout_tiles` property. Each element will have `visualization_id` and `size`:

    pb_obj = Liveboard(ts.export_tml(guid=pb_guid))
    tiles = pb_obj.layout_tiles  # This makes a copy, so you will have to reset pb_obj.layout_tiles = tiles later to save your changes to the object
    for tile in tiles:
        if tiles['size'] == pb_obj.TileSizes.MEDIUM:
            tile['size'] = pb_obj.TileSizes.LARGE
    # Adjust the order using regular Python List methods 
    tiles.reverse()  # Flips the order
    # You must set the Liveboard object property to the new version
    pb_obj.layout_tiles = tiles

#### Removing an Answer from a Liveboard
Removing an Answer requires removing the Answer section and the reference in the layout section. For this reason, the action has been encapsulated into a method:

`Liveboard.remove_answer_by_index(index: int)`

The index refers to the order of the Answer in the Answer section, rather than the visible order, which is determined in the layout section. You'll have to look at the TML of the Liveboard to determine the index necessary to do what you want (Answers can have the same name and definition so it's hard to identify them any other way than their order).

`Liveboard.remove_answer_by_layout_index(index: int)`

looks to the Layout section, finds the Answer at the given index in that section, then removes in both places.

#### Adding an Answer to a Liveboard
Because Answers use the same TML when stored separately or on a Liveboard, you can add an Answer object right into an existing Liveboard. You must specify the layout order and sizing (or it will default to the end and default size).

The `Liveboard.add_answer_by_index(answer: Answer, index: int, tile_size: str)` method performs all the necessary insertions. You pass an Answer object, the index for layout, and a size, and it adds the correct sections to the Liveboard TML.

In this example, we'll grab an existing Answer and add it to a Liveboard:

    a_id = ts.answer.find_guid(name='Answer 1')
    # Create the Answer object
    a_obj = Answer(tml_dict=ts.tml.export_tml(guid=a_id))
    
    pb_id = ts.liveboard.find_guid(name='My Liveboard')
    pb_obj = Liveboard(tml_dict=ts.tml.export_tml(guid=pb_id))
    #  Add the Answer    
    pb_obj.add_answer_by_index(answer=a_obj, index=4, tile_size=pb_obj.TileSizes.EXTRA_LARGE)

### Answer class
An Answer is a Saved Search, and is loaded with the Search bar and other editing features visible. It is a single table or visualization with many options.

As mentioned above in the Liveboard class, the TML for an independent Answer is identical to an Answer within a Liveboard, so the same object type is used for both.

    answer_obj = Answer(ts.export_tml(guid=answer_guid))
    print(answer_obj.search_query)
    answer_obj.set_table_mode()
    answer_obj.description = 'This is a great answer'

The Answer class has an ENUM of all the possible chart types:

`Answer.ChartTypes`

Whether the Answer displays as a Chart or a Table is the `display_mode` property, which is directly accessible but has also been wrapped with:

    Answer.set_chart_mode()
    Answer.set_table_mode()

### Changing References (Switching a Liveboard to a different Worksheet, Worksheet to different tables etc.)
One of the primary use cases of TML is taking an existing object (a Liveboard for example) and either making a copy that maps to a different Worksheet, or just updating the original. 

The most effective way to get the GUIDs necessary to change references is to export the associated_objects when you first downloaded a TML file and added the `fqn` property using `add_fqns_from_name_guid_map()` method. 

There are object references within the TML, that need GUIDs from the Server. Using the REST API commands, you can get these GUIDs.

This extends our example from above, pulling the guid of a Worksheet and replacing it within the TML object.

    # Find the GUID of the Worksheet to switch to
    new_worksheet_name = 'Worksheet We are Switching To'
    ws_guid = ts.worksheet.find_guid(new_worksheet_name)
  
    # You need to specify the original Worksheet name, in case not all Answers use
    # that particular WS. It will only replace where it finds a match
    o_lb_ws_name = 'Original WS'

    # Switch Liveboard to the new worksheet
    lb.update_worksheet_on_all_answers_by_fqn(original_worksheet_name=o_pb_ws_name, new_worksheet_guid_for_fqn=wg_guid)

Every TML class (see section below) has methods for swapping in FQNs in place of the 'pretty names'. There is an example called `tml_create_new_from_existing.py` which shows a full process of remapping from Tables to Worksheets through Liveboards and Answers. 


### Note on JOINs (POSSIBLY DEPRECATED)
JOINs between tables in ThoughtSpot are objects in the system that exist with their own unique IDs. At the current time, they are named automatically and the names are not unique by default.

To ensure that TML publishing works, you should manually add some type of random number or alphanumeric to the end of the automatically generated JOIN name so that every JOIN has a unique name.

Ex. If you have a JOIN named "DIM_TABLE_1_DIM_TABLE_2", press "Edit" and rename to: "DIM_TABLE_1_DIM_TABLE_2_z1Tl" or some other pattern that guarantees uniqueness.
