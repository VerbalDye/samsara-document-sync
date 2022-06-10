#import all modules for project
from urllib import response
import requests
from PIL import Image 
import keys
import json
import datetime

# samsara api endpoint
url = "https://api.samsara.com/fleet/documents?"

# headers
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + keys.SAMSARA_API_KEY
}

endTime = datetime.datetime.now()
startTime = endTime - datetime.timedelta(1)

urlTime = "endTime=" + endTime.strftime('%Y-%m-%dT04:00:00Z') + "&startTime=" + startTime.strftime('%Y-%m-%dT04:00:00Z')

def api_call(URL):
    response = requests.get(URL, headers=headers)

    return json.loads(response.text)

parsedResponse = api_call(url + urlTime)

for index, document in enumerate(parsedResponse["data"]):
    for field in document["fields"]:
        try:
            imageUrl = field["value"]["scannedDocumentValue"][0]["url"]
            responseImage = requests.get(imageUrl)
            open('output\document_' + str(index) + '.jpg', 'wb').write(responseImage.content)
            test_1 = Image.open(r'output\document_' + str(index) + '.jpg')
            im_1 = test_1.convert('RGB')
            im_1.save(r'output\processed\pdf_' + str(index) + '.pdf')
        except KeyError:
            print("")