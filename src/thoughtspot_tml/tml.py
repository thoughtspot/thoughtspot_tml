from typing import Optional, Dict, List # , OrderedDict
import typing
from random import randrange
import random
import string
from collections import OrderedDict
import re

import oyaml as yaml
# TML class works on TML as a Python Dict or OrderedDict structure (i.e. the result of a JSON.loads() or oyaml.load() )


class TML:
    def __init__(self, tml_ordereddict: [typing.OrderedDict, Dict]):
        self.tml = tml_ordereddict
        # Answers within a Pinboard just have an "id"
        if 'guid' in tml_ordereddict:
            self.guid = tml_ordereddict["guid"]
        elif 'id' in tml_ordereddict:
            self.guid = tml_ordereddict["id"]

        self.content_type = None
        # TML file outer is always a guid, then the type of Object being modeled
        for key in self.tml:
            if key in ["guid", "id"]:
                continue
            else:
                self.content_type = key
                # Some answers have additional properties later ("display_headline_column"), so need to break after
                # the actual content_type is found to not overwrite
                break

    def _first_level_property(self, property_key):
        if property_key in self.content:
            return self.content[property_key]
        return None

    def _second_level_property(self, first_level_key, second_level_key):
        if second_level_key in self.content[first_level_key]:
            return self.content[first_level_key][second_level_key]
        else:
            return None

    @property
    def content(self):
        if self.content_type in self.tml:
            return self.tml[self.content_type]
        else:
            return None

    @property
    def content_name(self):
        if "name" in self.tml[self.content_type]:
            return self.tml[self.content_type]["name"]
        else:
            return None

    @content_name.setter
    def content_name(self, new_name: str):
        self.content["name"] = new_name

    def remove_guid(self):
        if 'guid' in self.tml:
            del self.tml['guid']

    @property
    def guid(self):
        if 'guid' in self.tml:
            return self.tml['guid']
        else:
            return None

    @guid.setter
    def guid(self, new_guid: str):
        self.tml['guid'] = new_guid

    def remove_calendars(self):
        """Removes any references to customer calendars, which aren't supported on Embrace tables."""
        # The above comment may no longer be true in recent versions
        try:
            # Remove from the content.
            for col in self.content['worksheet_columns']:
                   props = col['properties']
                   if 'calendar' in props.keys():
                       del[props['calendar']]

        except IndexError as e:  # in case something is off.
            print(e)

    def __str__(self):
        strval = ""
        for (k,v) in self.tml.items():
            if not k.startswith("__"):
                strval += f"{k}: {v}\n"
        return strval


class Worksheet(TML):
    def __init__(self, tml_ordereddict: [typing.OrderedDict, Dict]):
        super().__init__(tml_ordereddict=tml_ordereddict)

    @staticmethod
    def generate_tml_from_scratch(worksheet_name: str, table_name: str, table_path_id: str = None):
        # Default to simply adding "_1" to the name
        if table_path_id is None:
            table_path_id = table_name + "_1"
        template = """
worksheet:
  name: {name}
  tables:
  - name: {table_name}
  table_paths:
  - id: {table_path_id}
    table: {table_name}
    join_path:
     - {{}}
  worksheet_columns:
  properties:
    is_bypass_rls: false
    join_progressive: true
"""
        return template.format(name=worksheet_name, table_name=table_name, table_path_id=table_path_id)

    # TML files do not include the GUIDs of related objects. But this can be retrieved from export_associated=true
    # option of the tml/export command. This takes a dictionary of Object Name: GUID generated from that REST API
    def add_fqns_from_name_guid_map(self, name_guid_map: Dict):
        for a in self.tables:
            table_name = a['name']
            if table_name in name_guid_map:
                a['fqn'] = name_guid_map[table_name]

    @property
    def description(self):
        key = "description"
        return self._first_level_property(key)

    @description.setter
    def description(self, new_value: str):
        key = "description"
        self.content[key] = new_value

    @property
    def properties(self):
        key = "properties"
        return self.content[key]

    @property
    def is_bypass_rls_flag(self):
        first_level_key = "properties"
        second_level_key = "is_bypass_rls"
        return self._second_level_property(first_level_key, second_level_key)

    @is_bypass_rls_flag.setter
    def is_bypass_rls_flag(self, new_value: bool):
        first_level_key = "properties"
        second_level_key = "is_bypass_rls"
        self.content[first_level_key][second_level_key] = str(new_value).lower()

    @property
    def join_progressive_flag(self):
        first_level_key = "properties"
        second_level_key = "join_progressive"
        return self._second_level_property(first_level_key, second_level_key)

    @join_progressive_flag.setter
    def join_progressive_flag(self, new_value: bool):
        first_level_key = "properties"
        second_level_key = "join_progressive"
        self.content[first_level_key][second_level_key] = str(new_value).lower()

    @property
    def tables(self):
        key = "tables"
        return self._first_level_property(key)

    @property
    def joins(self):
        key = "joins"
        return self._first_level_property(key)

    @property
    def table_paths(self):
        key = "table_paths"
        return self._first_level_property(key)

    @property
    def worksheet_columns(self):
        key = 'worksheet_columns'
        if self.content[key] is None:
            self.content[key] = []
        return self._first_level_property(key)

    @staticmethod
    # Only a bare minimum of properties
    def create_worksheet_column(column_display_name: str, ws_table_path_id: str, table_column_name: str,
                                column_type='ATTRIBUTE', index_type='DONT_INDEX'):

        column_id = "{}::{}".format(ws_table_path_id, table_column_name)
        column_template = OrderedDict({'name': column_display_name,
                                        'column_id': column_id,
                                        'properties': {
                                         'column_type': column_type,
                                          'index_type': index_type
                                        }
                                       })

        return column_template

    def add_worksheet_column(self, column_dict):
        self.worksheet_columns.append(column_dict)

    # Add all in a list
    def add_worksheet_columns(self, column_dict_list: List):
        for c in column_dict_list:
            self.add_worksheet_column(c)

    def change_table_by_fqn(self, original_table_name: str, new_table_guid: str):
        tables = self.tables
        for t in tables:
            if t["name"] == original_table_name:
                # Add fqn reference to point to new worksheet
                t["fqn"] = new_table_guid
                # Change id to be previous name
                t["id"] = t["name"]
                # Remove the original name parameter
                del t["name"]

    def remap_tables_to_new_fqn(self, name_to_fqn_map: Dict):
        # joins_with is an Array of JOIN information
        for a in self.tables:
            table_name = a['name']
            if table_name in name_to_fqn_map:
                a['fqn'] = name_to_fqn_map[table_name]



class View(TML):
    def __init__(self, tml_ordereddict: [typing.OrderedDict, Dict]):
        super().__init__(tml_ordereddict=tml_ordereddict)
    pass

    # TML files do not include the GUIDs of related objects. But this can be retrieved from export_associated=true
    # option of the tml/export command. This takes a dictionary of Object Name: GUID generated from that REST API
    def add_fqns_from_name_guid_map(self, name_guid_map: Dict):
        for a in self.tables:
            table_name = a['name']
            if table_name in name_guid_map:
                a['fqn'] = name_guid_map[table_name]


class Table(TML):
    def __init__(self, tml_ordereddict: [typing.OrderedDict, Dict]):
        super().__init__(tml_ordereddict=tml_ordereddict)

    @staticmethod
    def generate_tml_from_scratch(connection_name: str, db_name: str, schema: str, db_table: str,
                                  table_name: str = None):
        template = """
table:
  name: {name}
  db: {db}
  schema: {schema}
  db_table: {db_table}
  connection:
    name: {connection_name}
  columns:
        """
        # Allow override to pretty name
        if table_name is None:
            table_name = db_table
        return template.format(connection_name=connection_name, name=table_name, db=db_name, schema=schema,
                               db_table=db_table)

    @property
    def db_name(self):
        key = "db"
        return self._first_level_property(key)

    @db_name.setter
    def db_name(self, new_value: str):
        key = "db"
        self.content[key] = new_value

    @property
    def schema(self):
        key = "schema"
        return self._first_level_property(key)

    @schema.setter
    def schema(self, new_value: str):
        key = "schema"
        self.content[key] = new_value

    @property
    def db_table(self):
        key = "db_table"
        return self._first_level_property(key)

    @db_table.setter
    def db_table(self, new_value: str):
        key = "db_table"
        self.content[key] = new_value

    @property
    def connection(self):
        if "connection" in self.content:
            return self.content["connection"]
        else:
            return None

    @property
    def connection_name(self):
        first_level_key = "connection"
        second_level_key = "name"
        if second_level_key in self.content[first_level_key]:
            return self.content[first_level_key][second_level_key]
        else:
            return None

    @connection_name.setter
    def connection_name(self, new_value: str):
        first_level_key = "connection"
        second_level_key = "name"
        self.content[first_level_key][second_level_key] = new_value

    @property
    def connection_type(self):
        first_level_key = "connection"
        second_level_key = "type"
        if second_level_key in self.content[first_level_key]:
            return self.content[first_level_key][second_level_key]
        else:
            return None

    @connection_type.setter
    def connection_type(self, new_value: str):
        first_level_key = "connection"
        second_level_key = "type"
        self.content[first_level_key][second_level_key] = new_value

    def replace_connection_name_with_fqn(self, fqn_guid: str):
        first_level_key = "connection"
        second_level_key = "name"
        del self.content[first_level_key][second_level_key]
        self.content[first_level_key]['fqn'] = fqn_guid

    @property
    def columns(self):
        # Create empty array for generating from scratch
        if self.content["columns"] is None:
            self.content["columns"] = []
        return self.content["columns"]

    @staticmethod
    def create_column(column_display_name: str, db_column_name: str, column_data_type: str,
                      column_type='ATTRIBUTE', index_type='DONT_INDEX'):
        column_template = OrderedDict({'name': column_display_name,
                                        'db_column_name': db_column_name,
                                        'properties': {
                                         'column_type': column_type,
                                          'index_type': index_type
                                        },
                                        'db_column_properties': {
                                          'data_type': column_data_type
                                        }
                                       })

        return column_template

    def add_column(self, column_dict):
        self.columns.append(column_dict)

    # Adds all if passed a list
    def add_columns(self, column_dict_list: List):
        for c in column_dict_list:
            self.add_column(c)

    # Connection names are unique and thus don't require FQN
    def change_connection_by_name(self, original_connection_name: str, new_connection_name: str):
        c = self.connection
        if self.connection_name == original_connection_name:
            self.connection_name = new_connection_name

    @property
    def joins(self):
        first_level_key = "joins_with"
        return self.content[first_level_key]

    # When publishing a large set of tables, it may not be possible to replicate the JOINs initially because referenced
    # tables may not exist yet from the publishing process. This removes the section, and later you can add them
    def remove_joins(self):
        if 'joins_with' in self.content:
            del self.content['joins_with']

    # RLS rules reference other tables which may not exist yet, similar to the joins_with section
    def remove_rls_rules(self):
        if 'rls_rules' in self.content:
            del self.content['rls_rules']

    def remap_joins_to_new_fqn(self, name_to_fqn_map: Dict):
        # joins_with is an Array of JOIN information
        if 'joins_with' in self.content:
            for a in self.content['joins_with']:
                table_name = a['destination']['name']
                if table_name in name_to_fqn_map:
                    a['destination']['fqn'] = name_to_fqn_map[table_name]
                    del a['destination']['name']

    def remap_rls_rules_tables_to_new_fqn(self, name_to_fqn_map: Dict):
        # rules_rules is root element
        #if 'rls_rules' in self.content:
        #    if 'tables' in self.content['rls_rules']:
        pass

    def randomize_join_names(self, length=6):

        if 'joins_with' in self.content:
            for a in self.content['joins_with']:
                random_append = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
                a['name'] = a['name'] + "_" + random_append


class Answer(TML):
    def __init__(self, tml_ordereddict: [typing.OrderedDict, Dict]):
        super().__init__(tml_ordereddict=tml_ordereddict)

        class ChartTypes:
            COLUMN = 'COLUMN'
            BAR = 'BAR'
            LINE = 'LINE'
            PIE = 'PIE'
            SCATTER = 'SCATTER'
            BUBBLE = 'BUBBLE'
            STACKED_COLUMN = 'STACKED_COLUMN'
            AREA = 'AREA'
            PARETO = 'PARETO'
            GEO_AREA = 'GEO_AREA'
            GEO_BUBBLE = 'GEO_BUBBLE'
            GEO_HEATMAP = 'GEO_HEATMAP'
            GEO_EARTH_BAR = 'GEO_EARTH_BAR'
            GEO_EARTH_AREA = 'GEO_EARTH_AREA'
            GEO_EARTH_GRAPH = 'GEO_EARTH_GRAPH'
            GEO_EARTH_BUBBLE = 'GEO_EARTH_BUBBLE'
            GEO_EARTH_HEATMAP = 'GEO_EARTH_HEATMAP'
            WATERFALL = 'WATERFALL'
            TREEMAP = 'TREEMAP'
            HEATMAP = 'HEATMAP'
            STACKED_AREA = 'STACKED_AREA'
            LINE_COLUMN = 'LINE_COLUMN'
            FUNNEL = 'FUNNEL'
            LINE_STACKED_COLUMN = 'LINE_STACKED_COLUMN'
            PIVOT_TABLE = 'PIVOT_TABLE'
            SANKEY = 'SANKEY'
            GRID_TABLE = 'GRID_TABLE'
            SPIDER_WEB = 'SPIDER_WEB'
            WHISKER_SCATTER = 'WHISKER_SCATTER'
            STACKED_BAR = 'STACKED_BAR'
            CANDLESTICK = 'CANDLESTICK'
        self.CHART_TYPES = ChartTypes

    # TML files do not include the GUIDs of related objects. But this can be retrieved from export_associated=true
    # option of the tml/export command. This takes a dictionary of Object Name: GUID generated from that REST API
    def add_fqns_from_name_guid_map(self, name_guid_map: Dict):
        for a in self.tables:
            table_name = a['name']
            if table_name in name_guid_map:
                a['fqn'] = name_guid_map[table_name]

    @property
    def description(self):
        key = "description"
        return self._first_level_property(key)

    @description.setter
    def description(self, new_value: str):
        key = "description"
        self.content[key] = new_value

    @property
    def display_mode(self):
        key = "display_mode"
        return self._first_level_property(key)

    @display_mode.setter
    def display_mode(self, new_value: str):
        key = "display_mode"
        self.content[key] = new_value

    # Helper functions since the values are non-obvious
    def set_chart_mode(self):
        self.display_mode = 'CHART_MODE'

    def set_table_mode(self):
        self.display_mode = 'TABLE_MODE'

    @property
    def search_query(self):
        key = "search_query"
        return self._first_level_property(key)

    @search_query.setter
    def search_query(self, new_value: str):
        key = "search_query"
        self.content[key] = new_value

    @property
    def answer_columns(self):
        key = "answer_columns"
        return self._first_level_property(key)

    @property
    def tables(self):
        key = "tables"
        return self._first_level_property(key)

    @property
    def formulas(self):
        key = "formulas"
        return self._first_level_property(key)

    @property
    def chart(self):
        key = "chart"
        return self._first_level_property(key)

    # There is an 'fqn' parameter to use when replacing a worksheet reference
    # This is for when the names of the WS objects are the same after the transformation
    def change_worksheet_by_fqn(self, original_worksheet_name: str, new_worksheet_guid_for_fqn: str):
        tables = self.tables
        for t in tables:
            if t["name"] == original_worksheet_name:
                # Add fqn reference to point to new worksheet
                t["fqn"] = new_worksheet_guid_for_fqn
                # Change id to be previous name
                t["id"] = t["name"]
                # Remove the original name parameter
                del t["name"]

    # Allows for multiple mappings to be sent in
    def change_worksheets_by_fqn(self, name_to_guid_map: Dict[str, str]):
        tables = self.tables
        for t in tables:
            if t["name"] in name_to_guid_map:
                # Add fqn reference to point to new worksheet
                t["fqn"] = name_to_guid_map[t["name"]]
                # Change id to be previous name
                t["id"] = t["name"]
                # Remove the original name parameter
                del t["name"]

    # Full replace with no checks, whereas change_worksheet swaps without changing (expecting names to be the same)
    def replace_worksheet(self, new_worksheet_name: str, new_worksheet_guid_for_fqn: str):
        tables = self.tables
        for t in tables:
            # Add fqn reference to point to new worksheet
            t["fqn"] = new_worksheet_guid_for_fqn
            # Change id to be previous name
            t["id"] = new_worksheet_name
            # Remove the original name parameter
            del t["name"]


class Pinboard(TML):
    def __init__(self, tml_ordereddict: [typing.OrderedDict, Dict]):
        super().__init__(tml_ordereddict=tml_ordereddict)

    class TileSizes:
        EXTRA_SMALL = 'EXTRA_SMALL'
        SMALL = 'SMALL'
        MEDIUM = 'MEDIUM'
        LARGE = 'LARGE'
        LARGE_SMALL = 'LARGE_SMALL'
        MEDIUM_SMALL = 'MEDIUM_SMALL'
        EXTRA_LARGE = 'EXTRA_LARGE'

    @property
    def visualizations(self):
        # Should these be "Answer" objects
        if 'visualizations' in self.content:
            return self.content["visualizations"]
        else:
            return []

    @property
    def answers_as_objects(self) -> List[Answer]:
        v = self.visualizations
        answers = []
        for a in v:
            a_obj = Answer(a)
            answers.append(a_obj)
        return answers

    def remove_answer_by_index(self, index: int):
        # Index is of the Answer in the Answer section, and then the reference in the layout is found and removed
        # Thus the order may differ from what is seen through ThoughtSpot, because the layout section determines visible
        # order.

        # Needs to delete both the Answer and its reference in the Layout Tiles
        answer = self.content['visualizations'].pop(index)
        v_id = answer['id']
        new_layout_tiles = []
        layout_tiles = self.layout_tiles
        # Layout may not exist
        if layout_tiles is not None:
            for tile in layout_tiles:
                if tile['visualization_id'] == v_id:
                    continue
                else:
                    new_layout_tiles.append(tile)
            self.layout_tiles = new_layout_tiles

    def remove_answer_by_layout_index(self, index: int):
        # Index of the Answer in the layout section, and then the reference in the Answer section is found nad removed

        # Needs to delete both the Answer and its reference in the Layout Tiles

        layout_tiles = self.layout_tiles
        if layout_tiles is not None:
            layout_answer = layout_tiles.pop(index)
            self.layout_tiles = layout_tiles
            # Now find the answer in the visualizations
            answer = self.content['visualizations']
            v_id = layout_answer['visualization_id']
            new_answers = []
            for answer in self.visualizations:
                if answer['id'] == v_id:
                    continue
                else:
                    new_answers.append(answer)
            self.content['visualizations'] = new_answers

    def add_answer_by_index(self, answer: Answer, index: int, tile_size: str):
        # Answers need a Viz_ID to be mapped in the Tiles, replaced any GUID
        if 'guid' in answer.tml:
            del answer.tml['guid']
        # Make a new Viz ID with a number
        count_of_existing_answers = len(self.visualizations)
        # Add some random amount
        rand_int = randrange(5, 25, 1)
        new_num = count_of_existing_answers + rand_int
        new_id = "Viz_{}".format(new_num)
        # Assign ID to Answer
        answer.tml['id'] = new_id
        # Add Answer to Pinboard
        self.content['visualizations'].append(answer.tml)

        # Add to Layout Tiles in the right order, if they exist
        layout_tiles = self.layout_tiles
        if layout_tiles is not None:
            new_tile = {"visualization_id": new_id, "size": tile_size}
            layout_tiles.insert(index, new_tile)
            print(layout_tiles)
            self.layout_tiles = layout_tiles

    @property
    def layout_tiles(self):
        first_level_key = "layout"
        second_level_key = "tiles"
        # it's possible that 'layout' property doesn't exist, if no changes have been made from default
        if first_level_key in self.content:
            return self.content[first_level_key][second_level_key]
        else:
            return None

    @layout_tiles.setter
    def layout_tiles(self, new_tiles):
        first_level_key = "layout"
        second_level_key = "tiles"
        if first_level_key in self.content:
            self.content[first_level_key][second_level_key] = new_tiles
        # If the 'layout':'tiles' key doesn't exist, should we create it? Would require replicating the

    # The rule here is that the none of the Answers can connect to separate Worksheets with the same display name
    def add_fqns_from_name_guid_map(self, name_guid_map: Dict):
        for a in self.visualizations:
            answer = Answer(a)
            answer.add_fqns_from_name_guid_map(name_guid_map=name_guid_map)

    # Pass through to allow hitting all Answers contained with a single pinboard
    # You can also do this individually if working the objects one by one
    def update_worksheet_on_all_visualizations_by_fqn(self, original_worksheet_name: str, new_worksheet_guid_for_fqn: str):
        for a in self.visualizations:
            answer = Answer(a)
            answer.change_worksheet_by_fqn(original_worksheet_name=original_worksheet_name,
                                           new_worksheet_guid_for_fqn=new_worksheet_guid_for_fqn)

    def remap_worksheets_to_new_fqn(self, name_to_guid_map: Dict[str, str]):
        for a in self.visualizations:
            answer = Answer(a)
            answer.change_worksheets_by_fqn(name_to_guid_map=name_to_guid_map)

    def replace_worksheet_on_all_visualizations(self, new_worksheet_name: str, new_worksheet_guid_for_fqn: str):
        for a in self.visualizations:
            answer = Answer(a)
            answer.replace_worksheet(new_worksheet_name=new_worksheet_name,
                                     new_worksheet_guid_for_fqn=new_worksheet_guid_for_fqn)

# Liveboard is new name for Pinboard. TML file structure still references pinboard so there are
# no difference at this time 2022-02-03
class Liveboard(Pinboard):
    pass


###
# YAML loader and dumper class
###

class YAMLTML:
    def __init__(self):
        pass

    # Special method to match the initial output from PyYAML with the output from ThoughtSPot itself
    # Allows manipulation as object then dump to a file with minimum changes tracked in Git
    @staticmethod
    def dump_tml_object(tml_obj, tml_export_width=10000) -> str:
        # The width property must be large to not introduce line breaks into long formulas
        dump_yaml_string = yaml.dump(tml_obj.tml, Dumper=yaml.Dumper, width=tml_export_width)

        # The 'expr' tag in a worksheet is always double-quoted, but PyYAML output does not do
        re_pattern = "(expr: )(.+)\n"

        def double_quote_expr_values(matchobj):
            yaml_key = matchobj.group(1)
            yaml_value = matchobj.group(2)
            # Need to escape any double quotes with a backslash, to handle the possibility of quoted text in string calc
            yaml_value = yaml_value.replace('"', '\\"')
            return '{}"{}"\n'.format(yaml_key, yaml_value)

        final_yaml = re.sub(re_pattern, double_quote_expr_values, dump_yaml_string)
        return final_yaml

    # We use oyaml to load as an OrderedDict to maintain the order for identical output after manipulation
    @staticmethod
    def load_string(tml_yaml_str) -> OrderedDict:
        return yaml.load(tml_yaml_str, Loader=yaml.Loader)

    # Factory method to return the correct object type
    @staticmethod
    def get_tml_object(tml_yaml_str):
        tml_od = YAMLTML.load_string(tml_yaml_str)
        # TML file outer is always a guid, then the type of Object being modeled
        content_type = 'tml'
        for key in tml_od:
            if key in ["guid", "id"]:
                continue
            else:
                content_type = key

        if content_type == 'tml':
            return TML(tml_od)
        elif content_type == 'table':
            return Table(tml_od)
        elif content_type == 'worksheet':
            return Worksheet(tml_od)
        elif content_type == 'view':
            return View(tml_od)
        elif content_type == 'liveboard':
            return Liveboard(tml_od)
        elif content_type == 'pinboard':
            return Liveboard(tml_od)
        elif content_type == 'answer':
            return Answer(tml_od)

    # Factory method to return the object type as string
    @staticmethod
    def get_tml_type(tml_yaml_str) -> str:
        tml_od = YAMLTML.load_string(tml_yaml_str)
        # TML file outer is always a guid, then the type of Object being modeled
        content_type = 'tml'
        for key in tml_od:
            if key in ["guid", "id"]:
                continue
            else:
                content_type = key
        return content_type

