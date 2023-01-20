import urllib.request
import urllib.parse
import json
import base64


##################################################################################################
#####################  Authentication Section From Here  #########################################
##################################################################################################
secret = input("Enter the client secret: ")
headers = {}

def setAuthorizationHeader():
    secret_key = '2dC3aXnN:' + secret
    secret_key_bytes = secret_key.encode('ascii')
    secret_key_b64bytes = base64.b64encode(secret_key_bytes)
    secret_key_b64string = secret_key_b64bytes.decode('ascii')
    data = {'grant_type': 'client_credentials'}
    data = urllib.parse.urlencode(data)
    data = data.encode('ascii')
    request = urllib.request.Request('https://users.talis.com/oauth/tokens', data=data, method="POST")
    request.add_header('Authorization', 'Basic ' + secret_key_b64string)
    response = urllib.request.urlopen(request)
    response_text = response.read().decode('utf8')
    response_json = json.loads(response_text)
    token = response_json["access_token"]
    headers['Authorization'] = "Bearer " + token

def setUserHeader():
    headers['X-Effective-User'] = '7CcTgKkgj3yrkfglWs9XwQ' ## This sets me as the user!

setAuthorizationHeader()
setUserHeader()


####################################################################################################
#####################  Re-usable Code Section From Here  ###########################################
####################################################################################################
api_base = "https://rl.talis.com/3/solent/"

def createRequestObject(url, body, method):
    if body:
        jsondata = json.dumps(body)
        jsondataasbytes = jsondata.encode('utf-8')        
        request = urllib.request.Request(url, data=jsondataasbytes, headers=headers, method=method)
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        request.add_header('Content-Length', len(jsondataasbytes))
    else:
        request = urllib.request.Request(url, data=None, headers=headers, method=method)
    return request

def makeRequest(requestObject):
    try:
        response = urllib.request.urlopen(requestObject)
        response_text = response.read().decode('utf8')
        response_json = json.loads(response_text)
        return response_json
    except Exception as e:
        print(str(e))
        print(e.read())
        
        
##################################################################################################
################  Real Functions From Here Onwards  ##############################################
##################################################################################################
def getListEtag(list_id):
    list_etag = ""
    url = api_base + "draft_lists/" + list_id
    request = urllib.request.Request(url, headers=headers)
    response = makeRequest(request)
    list_etag = response['data']['meta']['list_etag']
    return list_etag

def getListFromItem(item):
    item_json = getItem(item)
    list_id = item_json['data']['relationships']['list']['data']['id']
    return(list_id)

def getListItems(list_id):
    full_data = []
    url = api_base + "lists/" + list_id + "/items?page[limit]=200"
    lastPage = False
    while not lastPage:
        request = urllib.request.Request(url, headers=headers)
        response = makeRequest(request)
        for datum in response['data']:
            full_data.append(datum)
        try:
            url = response['links']['next']
        except:
            lastPage = True
    return full_data

def getList(list_id):
    url = api_base + "lists/" + list_id
    request = urllib.request.Request(url, headers=headers)
    response = makeRequest(request)
    return response

def getItem(item_id):
    url = api_base + "items/" + item_id + "?include=list"
    request = urllib.request.Request(url, headers=headers)
    response = makeRequest(request)
    return response

def getResource(resource_id):
    url = api_base + "resources/" + resource_id
    request = urllib.request.Request(url, headers=headers)
    response = makeRequest(request)
    return response

def updateResourceLinkAndLCN(resource_id, lcn, link):
    url = api_base + "resources/" + resource_id
    body = {"data":
                {"type":"resources",
                "id":resource_id,
                "attributes":{
                    "online_resource":{
                        "source":"uri",
                        "link":link},
                    "web_addresses":[link],
                    "lcn":lcn}}}
    request = createRequestObject(url, body, "PATCH")
    response = makeRequest(requestObject)
    return response

def updateResourceLinkOnly(resource_id, link):
    url = api_base + "resources/" + resource_id
    body = {"data":
                {"type":"resources",
                "id":resource_id,
                "attributes":{
                    "online_resource":{
                        "source":"uri",
                        "link":link},
                    "web_addresses":[link]}}}
    request = createRequestObject(url, body, "PATCH")
    response = makeRequest(requestObject)
    return response

def updateResource(resource_id, body_with_changes):
    url = api_base + "resources/" + resource_id
    request = createRequestObject(url, body_with_changes, "PATCH")
    response = makeRequest(requestObject)
    return response

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
    request = createRequestObject(url, body, "POST")
    response = makeRequest(request)
    return response

def createResource(body_for_new_resource):
    url = api_base + "resources"
    request = createRequestObject(url, body_for_new_resource, "POST")
    response = makeRequest(request)
    return response

def createDraftItem(body_for_new_item): 
    url = api_base + "draft_items"
    request = createRequestObject(url, body_for_new_item, "POST")
    response = makeRequest(request)
    return response

def deleteItem(item_id):
    list_id = getListFromItem(item_id)
    list_etag = getListEtag(list_id)
    body = {'meta':{
                'list_id':list_id,
                'list_etag':list_etag}}
    url = api_base + "draft_items/" + item_id
    request = createRequestObject(url, body, "DELETE")
    response = makeRequest(request)

def archiveList(list_id):
    url = api_base + "lists/" + list_id + "/archive"
    body = False
    request = createRequestObject(url, body, "POST")
    response = makeRequest(request)

def updateOwners(list_id, owner):
    url = api_base + "lists/" + list_id + "/relationships/owners"
    if owner == "James":
        body = {"data":[{"type":"users","id":"7CcTgKkgj3yrkfglWs9XwQ"}]}
    request = createRequestObject(url, body, "PATCH")
    response = makeRequest(request)
    return response
