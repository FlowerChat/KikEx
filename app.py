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
details_url = "https://maps.googleapis.com/maps/api/place/details/json"



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
    amp = str("&")
    ques= str("?")
    photo_ref = str("photoreference=")
    photo_width=str("maxwidth=1600")
    key_eq=str("key=")
    key_str=str(key)
    str_address="florist at"+str(address)

    
    
    
    
    
    #trying to retrieve pics
    
    search_payload = {"key":key, "query":str_address, "radius": 1500}
    search_req = requests.get(search_url, params=search_payload)
    search_json = search_req.json()
    gplace_id=search_json["results"][0]["place_id"][0]
    details_payload={"key":key, "placeid":gplace_id}
    details_req=requests.get(details_url, params=details_payload)
    details_json=details_req.json()
    #webadd=details_json["result"]["website"]
    #webadd_str=str(webadd)
    
    #photo_id = details_json["result"]["photos"][1]["photo_reference"]
    photo_id = search_json["results"][0]["photos"][0]["photo_reference"]
    #photo_link=photos_url+"?maxwidth=1600"+"&"+"photoreference="+photo_id+"&"+key
    
    photo_payload = {"key" : key, "maxwidth": 1600, "maxhight": 1600, "photoreference" : photo_id}
    photo_request = requests.get(photos_url, params=photo_payload)
    #final_pic=str(photo_request)
    
    final_pic=photos_url+ques+photo_width+amp+photo_ref+photo_id+amp+key_eq+"AIzaSyAb7Vnq1nSojwYd1TarHx_x6Gb4ti8bhVo"
    
    

    

    speech = "Here are the pictures of florists' work"


    print("Response:")
    print(speech)

    kik_message = [
        
        {
            "type": "picture",
            "picUrl": final_pic
            #"picUrl": "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=CnRtAAAATLZNl354RwP_9UKbQ_5Psy40texXePv4oAlgP4qNEkdIrkyse7rPXYGd9D_Uj1rVsQdWT4oRz4QrYAJNpFX7rzqqMlZw2h2E2y5IKMUZ7ouD_SlcHxYq1yL4KbKUv3qtWgTK0A6QbGh87GB3sscrHRIQiG2RrmU_jF4tENr9wGS_YxoUSSDrYjWmrNfeEHSGSc3FyhNLlBU&key=AIzaSyAb7Vnq1nSojwYd1TarHx_x6Gb4ti8bhVo"
        },
        
             {
            "type": "text",
            "body": webadd_str
        },
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
