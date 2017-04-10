#!/usr/bin/env python


import urllib
import json
import os

from flask import Flask, render_template, jsonify
import requests
from key import key
import imghdr
from flask import request
from flask import make_response

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
photos_url = "https://maps.googleapis.com/maps/api/place/photo"

#str = unicode(str, errors='ignore')


# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "show.florist":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    address = parameters.get("Address")
    zipcode = parameters.get("ZipCode")
    city = parameters.get("City")
    
    #trying to retrieve pics
    
    search_payload = {"key":key, "query":"Kvetinarstvi+rooseveltova+49+praha", "radius": 1000}
    search_req = requests.get(search_url, params=search_payload)
    search_json = search_req.json()
    photo_id = search_json["results"][0]["photos"][0]["photo_reference"]
    #photo_link=photos_url+"?maxwidth=1600"+"&"+"photoreference="+photo_id+"&"+key
    
    photo_payload = {"key" : key, "maxwidth": 1600, "maxhight": 1600, "photoreference" : photo_id}
    photo_request = requests.get(photos_url, params=photo_payload)
    

    

    speech = "Here are the pictures of florists' work"


    print("Response:")
    print(speech)

    kik_message = [
        
        {
            "type": "picture",
            "picUrl": "https://lh4.googleusercontent.com/-1wzlVdxiW14/USSFZnhNqxI/AAAAAAAABGw/YpdANqaoGh4/s1600-w400/Google%2BSydney"

        },
       # {
       #     "type": "text",
       #     "body": photo_request
       # },
        {
            "type": "picture",
            "picUrl": "http://fiorita.cz/wp-content/uploads/2017/03/kvetinarstvi-praha-jarni-kytice-tulipany-anemony-pryskyrniky.jpg"
        },
        {
            "type": "text",
            "body": "Here's an example of the Florist B work"
        },
        {
            "type": "picture",
            "picUrl": "http://fiorita.cz/wp-content/uploads/2017/03/spring-bouquet-jarni-kytka-web.jpg"
        },
        {
            "type": "text",
            "body": "Please choose Florist A or Florist B",
            "keyboards":[
                {"type": "suggested",
                "responses": [
                     {
                         "type": "text",
                         "body": "Florist A"
                     },
                     {
                         "type": "text",
                         "body": "Florist B"
                     }
                 ]
                }
            ]
        }
    ]


    print(json.dumps(kik_message))
    return {
        "speech": speech,
        "displayText": speech,
        "data": {"kik": kik_message},
        # "contextOut": [],
        "contextOut": [{"name":"choose-florist", "lifespan":2},{"name":"flowerchatline", "lifespan":5}]
    }

    



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

app.run(debug=True, port=port, host='0.0.0.0')
