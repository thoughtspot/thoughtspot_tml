from thoughtspot_tml import *
from thoughtspot_tml.utils import *

# Python request library for HTTP calls
from requests import *
# REST API library installable via pip
from thoughtspot_rest_api_v1 import *

# Examples of retrieving TML, loading into thoughtspot_tml objects, and serializing objects back into TML files
# Other examples, showing actual transformations on the TML objects, will refer to this example

# 'Publishing' a TML file to a ThoughtSpot instance uses the REST API /metadata/tml/import endpoint (V1 or V2.0)
# https://github.com/thoughtspot/thoughtspot_rest_api_v1_python library implements import in V1 or V2
# After publishing, you will want to retrieve the GUIDs from the response, for any newly created objects
# /security/metadata/share endpoint (V2.0) can be used to give access to the newly created objects
# For example, see https://github.com/thoughtspot/thoughtspot_rest_api_v1_python/blob/main/examples_v2/share_objects_access_control.py


# If you have TML files in a directory already:
def retrieve_from_disk():

    # Read from file when you know the object type
    tml_obj = Worksheet.load('/file/location/on/disk/something.worksheet.tml')

    # Read from an unknown type TML file using determine_tml_type() helper
    tml_cls = determine_tml_type(path="/tests/data/some_type_of_file.tml")
    tml_obj = tml_cls.load(path="/tests/data/DUMMY.worksheet.tml")
    if type(tml) is Worksheet:
        # Do things specific to the worksheet
        pass

    return tml_obj

def export_to_string(tml_object):
    # Each TML class has a .dumps(format_type="YAML") method to string
    tml_str = tml_object.dumps(format_type="YAML")
    print(tml_str)
    return tml_str

def export_to_disk(tml_object):
    # Each TML class has a .dump() method to serialize and save directly to disk

    # Example of programmatic naming with the GUID of the TML object. Make sure not to overwrite, and you may have
    # removed the GUID as well depending on what process you are going through
    export_path = "/tests/data/{}.worksheet.tml".format(tml_object.guid)

    tml_object.dump(path=export_path)
    return export_path

#
# REST API interactions below
# A simple implementations of REST functionality here based on thoughtspot_rest_api_v1 library (https://github.com/thoughtspot/thoughtspot_rest_api_v1_python)
# Please use the library for building more complex actions (it will save you time and effort)

def get_v2_api_token(session, thoughtspot_server, username, password, validity_time_in_sec=300):
    # V2.0 API needs a token
    endpoint = 'auth/token/full'
    url = '{}/api/rest/{}/{}'.format(thoughtspot_server, '2.0', endpoint)
    json_post_data = {
        'username': username,
        'password': password,
        'validity_time_in_sec': validity_time_in_sec
    }

    response = session.post(url=url, json=json_post_data)

    response.raise_for_status()
    token_response = response.json()
    token = token_response['token']
    return token


def retrieve_from_api_no_library():
    # ThoughtSpot has V1 and V2 REST APIs
    # Both have a /metadata/tml/export endpoint to get TML as a string, in the 'edoc' portion of the response
    # V1 can export in YAML or JSON, V2 currently only in JSON (eventually will support YAML)

    # http://github.com/thoughtspot/thoughtspot_rest_api_v1_python is pre-built library to handle REST API interactions

    thoughtspot_server = 'https://myinstance.thoughtspot.cloud'
    username = 'myUsername@company.com'
    password = 'apassword' # Find another way of storing to actually secure this

    # Create a session object to save some header settings etc.
    requests_session = requests.Session()
    api_headers = {'X-Requested-By': 'ThoughtSpot', 'Accept': 'application/json', 'Accept-Language': 'en_US'}
    requests_session.headers.update(api_headers)

    token = get_v2_api_token(session=requests_session, thoughtspot_server=thoughtspot_server, username=username,
                             password=password, validity_time_in_sec=300)

    # Add the token to the Session object for subsequent calls
    api_headers['Authorization'] = 'Bearer {}'.format(token)
    requests_session.headers.update(api_headers)

    # To find any particular object, use the 'metadata/search' endpoint
    # The request can be built with a large number of filtering and sorting options
    # See all of the fields in the V2.0 REST Playground

    metadata_search_request = {
        'metadata': {
            'type': 'Liveboard',
            'name_pattern': "DEV_%"
        },
        'create_by_user_identifiers': ['admin_a', 'admin_b'],
        'sort_options': {
            'field_name': 'MODIFIED',
            'order': 'DESC'
        }
    }

    endpoint = 'metadata/search'
    url = '{}/api/rest/{}/{}'.format(thoughtspot_server, '2.0', endpoint)
    response = requests_session.post(url=url, json=metadata_search_request)

    for item in response:
        guid = item['metadata_identifier']
        # even more details in
        headers = item['metadata_header']
        # headers['authorName']
        # headers['tags']
        break

    # Once you have a GUID, you can request the TML object

    # Set here manually, if you wanted to do repeated actions put in the loop above going through the search_response
    guid_to_retrieve = ''

    # This is the "long form". Eventually TYPE should not be required by the API when GUIDs are used (vs. names)
    md_request = [
        {
            'identifier': guid_to_retrieve,
            'type': 'LIVEBOARD'
        }
    ]

    endpoint = 'metadata/search'
    url = '{}/api/rest/{}/{}'.format(thoughtspot_server, '2.0', endpoint)
    tml_response = requests_session.post(url=url, json=md_request)
    # if you only requested 1 item, just access that one item in the List response. Otherwise loop to handle each
    tml_string = tml_response[0]['edoc']
    item_info = tml_response[0]['info']  # additional metadata

    # Load from string you know the object type
    tml_obj = Worksheet.loads(tml_string)

    # Read from an unknown type TML file using determine_tml_type() helper
    tml_cls = determine_tml_type(info=item_info)
    tml_obj = tml_cls.loads(tml_document=tml_string)
    if type(tml) is Worksheet:
        # Do things specific to the worksheet
        pass


# Example of the same workflow from above, using the thoughtspot_rest_api_v1 library
def retrieve_from_api_with_library():
    thoughtspot_server = 'https://myinstance.thoughtspot.cloud'
    username = 'myUsername@company.com'
    password = 'apassword' # Find another way of storing to actually secure this

    ts: TSRestApiV2 = TSRestApiV2(server_url=thoughtspot_server)
    try:
        auth_token_response = ts.auth_token_full(username=username, password=password, validity_time_in_sec=3000)
        ts.bearer_token = auth_token_response['token']
    except requests.exceptions.HTTPError as e:
        print(e)
        print(e.response.content)
        exit()

    metadata_search_request = {
        'metadata': {
            'type': 'Liveboard',
            'name_pattern': "DEV_%"
        },
        'create_by_user_identifiers': ['admin_a', 'admin_b'],
        'sort_options': {
            'field_name': 'MODIFIED',
            'order': 'DESC'
        }
    }
    search_response = ts.metadata_search(request=metadata_search_request)
    # Just an example of how to parse through the response for attributes. Identifier (guid) is what you need to
    # retrieve the TML response
    for item in search_response:
        guid = item['metadata_identifier']
        # even more details in
        headers = item['metadata_header']
        # headers['authorName']
        # headers['tags']

        #
        break


    # Once you have a GUID, you can request the TML object

    # Set here manually, if you wanted to do repeated actions put in the loop above going through the search_response
    guid_to_retrieve = ''

    # This is the "long form". Eventually TYPE should not be required by the API when GUIDs are used (vs. names)
    md_request = [
        {
            'identifier': guid_to_retrieve,
            'type': 'LIVEBOARD'
        }
    ]
    tml_response = ts.metadata_tml_export(metadata_ids=[], export_fqn=True, metadata_request=md_request)
    # if you only requested 1 item, just access that one item in the List response. Otherwise loop to handle each
    tml_string = tml_response[0]['edoc']
    item_info = tml_response[0]['info']  # additional metadata

    # Load from string you know the object type
    tml_obj = Worksheet.loads(tml_string)

    # Read from an unknown type TML file using determine_tml_type() helper
    tml_cls = determine_tml_type(info=item_info)
    tml_obj = tml_cls.loads(tml_document=tml_string)
    if type(tml) is Worksheet:
        # Do things specific to the worksheet
        pass