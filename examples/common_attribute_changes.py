from thoughtspot_tml import *
from thoughtspot_tml.utils import *

# Examples of the common attribute changes that people do on the various TML object types

# Not a fully functioning script, but a set of code snippets to be used in your own scripts

# Each example assumes you've created the appropriate TML object using .load() or .loads()
# see basic_input_output.py and the README for how to get the objects loaded from TML on disk or from API

# Modifies the Table object passed in, returns False if no changes were made
def change_table(t: Table) -> bool:
    # All properties can be accessed based on TML spec: https://docs.thoughtspot.com/cloud/latest/tml#syntax-tables

    # Simple map of existing database to new:
    db_map = {
        'old_test_db' : 'NEW_TEST_DB',
        'old_prod_db': 'NEW_PROD_DB'
    }

    # Only process if the database is found in the map
    if t.table.db in db_map:

        # If you want to guarantee a newly created Table object when uploading, set the guid to None
        t.guid = None  # Comment out if you are creating an UPDATE or moving to a new ThoughtSpot instance

        # connection has two properties, .name and .fqn . FQN takes a GUID (from the 'id' property of the connection)
        new_conn_guid = 'ddc6a4bc-312c-490d-912b-bd2b60b2ddd8'
        # If using an FQN, you can set name to None.
        t.table.connection.name = None
        t.table.connection.fqn = new_conn_guid

        # Alternatively, if there is an FQN present and you just want to switch using name, set fqn property to none
        # t.table.connection.name = '{New Connection Name}'
        # t.table.connection.fqn = None

        # get the Table's underlying connected details
        t.table.db = db_map[t.table_db]

        # Additional relevant properties you might modify
        # t.table.schema = ''
        # t.table.db_table  = ''

        cols = t.table.columns
        for c in cols:
            # Convert all lower-case column names to upper-case
            c.db_column_name = c.db_column_name.upper()
            # Set to not index if a string
            if c.data_type == 'VARCHAR':
                c.index_type = 'DONT_INDEX'
        return True

    else:
        return False


def change_worksheet(w: Worksheet):
    # All properties can be accessed based on TML spec: https://docs.thoughtspot.com/cloud/latest/tml#syntax-worksheets

    # Most frequent worksheet change is to switch the tables it is connected to
    # The disambiguate() helper function is designed to do this switch
    table_name_to_guid_map = {
        'table_name_1': '7fd39fdb-9dfe-4954-b5dd-9a5d846085b0',
        'table_name_2':  '99999999-9999-4999-9999-999999999999'
    }
    w = disambiguate(w, guid_mapping=table_name_to_guid_map)

    # You can also get to any of the columns and manipulate them
    for col in w.worksheet.worksheet_columns:

        # If you changed the format of column names in the connected tables, you may need to adjust the ID
        # This is in format <table_path>::<column_id_1> -- table_path defined in Worksheet, but '<column_id_1>' is
        # the 'name' property of the column in the Table object itself

        # Here we'll assume we upper-cased the names in the Table, and now must make that update in the Worksheet as well
        col_id = col.column_id
        col_id_split = col_id.split("::")
        col.column_id = "{}::{}".format(col_id_split[0], col_id_split[1].upper())

        # Add synonyms
        col.properties.synonyms = col.properties.synonyms + ",new synonym,second synonym"

    return True

def change_answer(a: Answer):
    # All properties can be accessed based on TML spec: https://docs.thoughtspot.com/cloud/latest/tml#syntax-answers

    # Most frequent answer change is to switch the worksheet it is connected to to a different one
    # The disambiguate() helper function is designed to do this switch
    ws_name_to_guid_map = {
        'ws_name_1': '7fd39fdb-9dfe-4954-b5dd-9a5d846085b0',
        'ws_name_2':  '99999999-9999-4999-9999-999999999999'
    }
    a = disambiguate(a, guid_mapping=ws_name_to_guid_map)

    return True


def change_liveboard(lb: Liveboard):
    # All properties can be accessed based on TML spec: https://docs.thoughtspot.com/cloud/latest/tml#syntax-liveboards

    # Most frequent Liveboard change is to switch the worksheet the vizes in it are connected to
    # Each viz can be connected to different worksheets (or tables) so passing a mapping with all possibilities
    # is the safest way to make this change

    # The disambiguate() helper function is designed to do this switch
    ws_name_to_guid_map = {
        'ws_name_1': '7fd39fdb-9dfe-4954-b5dd-9a5d846085b0',
        'ws_name_2': '99999999-9999-4999-9999-999999999999'
    }

    # You can also make a map that swaps GUID to GUID:
    ws_guid_to_guid_map = {
       '7fd39fdb-9dfe-4954-b5dd-9a5d846085b0': '99999999-9999-4999-9999-999999999999'
    }

    lb = disambiguate(lb, guid_mapping=ws_name_to_guid_map)

    lb.liveboard.description = "Updated description for the liveboard"

    # If you want to use to guarantee new object creation on import, delete guid property
    lb.guid = None

    return True