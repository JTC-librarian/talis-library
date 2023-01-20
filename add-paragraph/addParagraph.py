import talis
import uuid
import csv

def addParaToList(list_id):
    guid = uuid.uuid4()
    guid_string = str(guid)
    list_etag = talis.getListEtag(list_id)
    body = {
      "data": {
        "id": guid_string,
        "type": "items",
        "attributes": {
          "student_note": "<p><strong>Problems accessing a resource? </strong>Please report to us in three easy steps...</p><ol><li>Open the actions menu (the three vertical dots) for the affected resource.</li><li>Select 'Report broken link'. You will be prompted to sign in if needed.</li><li>Choose to request a response / describe the problem, or simply send the report.</li></ol>"
        },
        "relationships": {
          "container": {
            "data": {
              "id": list_id,
              "type": "lists"
            },
            "meta": {
              "index": 0
            }
          }
        }
      },
      "meta": {
        "list_etag": list_etag,
        "list_id": list_id
      }
    }
    talis.createDraftItem(body)

def checkListForPara(list_id):
    check = False
    item_list = talis.getListItems(list_id)
    for item in item_list:
        snote = item['attributes']['student_note']
        if "<p><strong>Problems accessing a resource?" in snote:
            check = True
    return check

def convertLinkToId(link):
    list_id = link.replace("http://solent.rl.talis.com/lists/", "")
    return list_id

### It is important that only published lists are used, as I need to publish them for my changes to apply,
### so using draft lists would end up publishing other people's changes as well.
infile = open('published_lists.20221104.csv', 'r', encoding='utf8', errors='ignore')
inreader = csv.reader(infile)
headers = next(inreader)
list_id_list = []
list_to_publish = []
for row in inreader:
    list_link = row[1]
    list_id = convertLinkToId(list_link)
    if list_id not in list_id_list:
        list_id_list.append(list_id)
print(len(list_id_list))
### Copy in/out section below for testing/not testing
#list_id_list = list_id_list[0:10]
#print(len(list_id_list))
###
count = 0
for list_id in list_id_list:
    count = count + 1
    print(count)
    if checkListForPara(list_id):
        pass
    else:
        addParaToList(list_id)
        list_to_publish.append(list_id)
print("Number of lists to publish after editing: " + str(len(list_to_publish)))
if len(list_to_publish) > 0:
    talis.publishLists(list_to_publish)
