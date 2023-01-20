import sys
sys.path.append('C:\\Users\\clarkj\\OneDrive - Solent University\\PythonModules')
import talis

def checkListForPara(list_id):
    item_id = ""
    check = False
    item_list = talis.getListItems(list_id)
    for item in item_list:
        snote = item['attributes']['student_note']
        if "<p><strong>Problems accessing a resource?" in snote:
            item_id = item['id']
    return item_id

def convertLinkToId(link):
    list_id = link.replace("http://solent.rl.talis.com/lists/", "")
    return list_id

# Can simply provide a list of lists below to check
infile = open('lists_to_check_and_delete.txt', 'r', encoding='utf8', errors='ignore')
list_id_list = []
list_to_publish = []
for line in infile:
    list_link = line.replace("\r", "")
    list_link = list_link.replace("\n", "")
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
    print(list_id)
    count = count + 1
    print(count)
    item_id = checkListForPara(list_id)
    if item_id != "":
        talis.deleteItem(item_id)
        list_to_publish.append(list_id)
print("Number of lists to publish after editing: " + str(len(list_to_publish)))
if len(list_to_publish) > 0:
    talis.publishLists(list_to_publish)
