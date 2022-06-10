#import all modules for project
from os import times
import requests
from PIL import Image 
from keys import *
import json
import datetime

# samsara api endpoint
url = "https://api.samsara.com/fleet/documents?"

# headers
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + SAMSARA_API_KEY
}

endTime = datetime.datetime.now()
startTime = endTime - datetime.timedelta(1)

urlTime = "endTime=" + endTime.strftime('%Y-%m-%dT04:00:00Z') + "&startTime=" + startTime.strftime('%Y-%m-%dT04:00:00Z')    

def processDocuments(documentId, endCursor):
    if endCursor is not None:
        URL = url + urlTime + "&documentTypeId=" + documentId + "&endCursor=" + endCursor
    else:
        URL = url + urlTime + "&documentTypeId=" + documentId

    response = requests.get(URL, headers=headers)

    parsedResponse = json.loads(response.text)

    for index, document in enumerate(parsedResponse["data"]):
        for field in document["fields"]:
            try:
                imageUrl = field["value"]["scannedDocumentValue"][0]["url"]
                responseImage = requests.get(imageUrl)
                timeString = datetime.datetime.now().strftime('%H%M%S%f')
                open('output\document_' + timeString + str(index) + '.jpg', 'wb').write(responseImage.content)
                test_1 = Image.open(r'output\document_'+ timeString + str(index) + '.jpg')
                im_1 = test_1.convert('RGB')
                im_1.save(r'output\processed\pdf_' + timeString + str(index) + '.pdf')
            except KeyError:
                print("")
    
    if(parsedResponse["pagination"]["hasNextPage"]):
        processDocuments(documentId, parsedResponse["pagination"]["endCursor"])

processDocuments(billOfLadingId, None)
# processDocuments(sendPaperworkId)
# processDocuments(departDeliveryId)