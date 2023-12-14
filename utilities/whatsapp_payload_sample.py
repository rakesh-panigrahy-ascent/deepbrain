import http.client
import json

conn = http.client.HTTPSConnection("gg1456.api.infobip.com")
payload = json.dumps({
    "messages": [
        {
            "from": "447860099299",
            "to": "919967912685",
            "messageId": "58baa939-c9e0-40e5-be3d-698b7318bca6",
            "content": {
                "templateName": "welcome_multiple_languages",
                "templateData": {
                    "body": {
                        "placeholders": ["Ratan "]
                    }
                },
                "language": "en"
            }
        }
    ]
})
headers = {
    'Authorization': 'App 074ea4f410d5e9fd4cae3f92b14b0b06-f3f259b1-96ab-4362-8e25-56ebd6c3dc9a',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
conn.request("POST", "/whatsapp/1/message/template", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))