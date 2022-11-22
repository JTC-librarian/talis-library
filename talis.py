import urllib.request
import urllib.parse
import json
import base64

secret = input("Enter the client secret: ")
api_base = "YOUR API BASE URL HERE" ## e.g., https://rl.talis.com/3/solent/
headers = {}

## This bit does the authorization. I have set it up so that the client ID is
### hardcoded in the file - put it in line 13 - and the Client Secret needs to
### be input each time you run a script (see line 6).
def setAuthorizationHeader():
    secret_key = 'YOUR CLIENT ID HERE' + ':' + secret
    secret_key_bytes = secret_key.encode('ascii')
    secret_key_b64bytes = base64.b64encode(secret_key_bytes)
    secret_key_b64string = secret_key_b64bytes.decode('ascii')
    data = {'grant_type': 'client_credentials'}
    data = urllib.parse.urlencode(data)
    data = data.encode('ascii')
    request = urllib.request.Request('https://users.talis.com/oauth/tokens', data=data)
    request.add_header('Authorization', 'Basic ' + secret_key_b64string)
    response = urllib.request.urlopen(request)
    response_text = response.read().decode('utf8')
    response_json = json.loads(response_text)
    token = response_json["access_token"]
    headers['Authorization'] = "Bearer " + token

## This bit sets the user. I have it hardcoded to my ID. You can get
### your ID from the All User Profile report on your tenancy, under the
### Talis Global User ID field.
def setUserHeader():
    headers['X-Effective-User'] = 'YOUR USER ID HERE'

setAuthorizationHeader()
setUserHeader()

def getListEtag(list_id):
    list_etag = ""
    url = api_base + "draft_lists/" + list_id
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    response_text = response.read().decode('utf8')
    response_json = json.loads(response_text)
    list_etag = response_json['data']['meta']['list_etag']
    return list_etag

def getListFromItem(item_id):
    item_json = getItem(item_id)
    list_id = item_json['data']['relationships']['list']['data']['id']
    return(list_id)

def getListItems(list_id):
    full_data = []
    url = api_base + "lists/" + list_id + "/items?page[limit]=200"
    lastPage = False
    while not lastPage:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        response_text = response.read().decode('utf8')
        response_json = json.loads(response_text)
        for datum in response_json['data']:
            full_data.append(datum)
        try:
            url = response_json['links']['next']
        except:
            lastPage = True
    return full_data

def getList(list_id):
    url = api_base + "lists/" + list_id
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    response_text = response.read().decode('utf8')
    response_json = json.loads(response_text)
    return response_json

def getItem(item_id):
    url = api_base + "items/" + item_id + "?include=list"
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    response_text = response.read().decode('utf8')
    response_json = json.loads(response_text)
    return response_json

def getResource(resource_id):
    url = api_base + "resources/" + resource_id
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    response_text = response.read().decode('utf8')
    response_json = json.loads(response_text)
    return response_json

def updateResourceLinkAndLCN(resource_id, lcn, link):
    url = api_base + "resources/" + resource_id
    print(link)
    body = {"data":{"type":"resources","id":resource_id,"attributes":{"online_resource":{"source":"uri","link":link},"web_addresses":[link],"lcn":lcn}}}
    print(body)
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')
    request = urllib.request.Request(url, data=jsondataasbytes, headers=headers, method='PATCH')
    request.add_header('Content-Type', 'application/json; charset=utf-8')
    request.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(request)
    response_text = response.read().decode('utf8')
    response_json = json.loads(response_text)
    return response_json

def updateResourceLinkOnly(resource_id, link):
    url = api_base + "resources/" + resource_id
    print(link)
    body = {"data":{"type":"resources","id":resource_id,"attributes":{"online_resource":{"source":"uri","link":link},"web_addresses":[link]}}}
    print(body)
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')
    request = urllib.request.Request(url, data=jsondataasbytes, headers=headers, method='PATCH')
    request.add_header('Content-Type', 'application/json; charset=utf-8')
    request.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(request)
    response_text = response.read().decode('utf8')
    response_json = json.loads(response_text)
    return response_json

def publishLists(list_of_lists):
    url = api_base + "bulk_list_publish_actions"
    list_of_list_dicts = []
    for list_id in list_of_lists:
        list_dict = {}
        list_dict['type'] = 'draft_lists'
        list_dict['id'] = list_id
        list_of_list_dicts.append(list_dict)
    body = {'data':{
                'type':'bulk_list_publish_actions',
                'relationships':{
                    'draft_lists':{
                        'data':list_of_list_dicts}}}}
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    request = urllib.request.Request(url, data=jsondataasbytes, headers=headers, method='POST')
    request.add_header('Content-Type', 'application/json; charset=utf-8')
    request.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(request)
    response_text = response.read().decode('utf8')
    response_json = json.loads(response_text)
    return response_json

def createDraftItem(body_dict): 
    url = api_base + "draft_items"
    jsondata = json.dumps(body_dict)
    jsondataasbytes = jsondata.encode('utf-8')
    request = urllib.request.Request(url, data=jsondataasbytes, headers=headers, method='POST')
    request.add_header('Content-Type', 'application/json; charset=utf-8')
    request.add_header('Content-Length', len(jsondataasbytes))
    try:
        response = urllib.request.urlopen(request)
        response_text = response.read().decode('utf8')
        response_json = json.loads(response_text)
    except Exception as e:
        print(str(e))
        print(e.read())

def deleteItem(item_id):
    list_id = getListFromItem(item_id)
    list_etag = getListEtag(list_id)
    body = {}
    body["meta"] = {}
    body["meta"]["list_id"] = list_id
    body["meta"]["list_etag"] = list_etag
    url = api_base + "draft_items/" + item_id
    response = requests.delete(url, json=body, headers=headers)
    print(response.text)
