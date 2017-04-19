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
import psycopg2



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
    ID=parameters.get("id")
    TimeStamp=parameters.get("timestamp")
    CustName=parameters.get("CustName")
    CustPhone=parameters.get("CustPhone")
    TypeofSale=parameters.get("TypeofSale")
    amp = str("&")
    ques= str("?")
    photo_ref = str("photoreference=")
    photo_width=str("maxwidth=1600")
    key_eq=str("key=")
    key_str=str(key)
    str_address="florist at"+str(address)

    
    
    
    
    
    #trying to retrieve pics
    
    search_payload = {"key":key, "query":str_address, "radius": 10000}
    search_req = requests.get(search_url, params=search_payload)
    search_json = search_req.json()
    gplace_id=search_json["results"][0]["place_id"]
    gplace_id2=search_json["results"][1]["place_id"]
    details_payload={"key":key, "placeid":gplace_id}
    details_payload2={"key":key, "placeid":gplace_id2}
    details_req=requests.get(details_url, params=details_payload)
    details_req2=requests.get(details_url, params=details_payload2)
    details_json=details_req.json()
    details_json2=details_req2.json()


    
    #webadd=details_json["result"]["website"]
    #webadd_str=str(webadd)
    
    photo_id = details_json["result"]["photos"][1]["photo_reference"]
    photo_id2=details_json2["result"]["photos"][1]["photo_reference"]
    name_shop1=details_json["result"]["name"]
    name_shop2=details_json2["result"]["name"]
    phone_shop1=details_json["result"]["international_phone_number"]
    phone_shop2=details_json2["result"]["international_phone_number"]
    form_add1=details_json["result"]["formatted_address"]
    form_add2=details_json2["result"]["formatted_address"]
    

    #website0=details_json["result"]["website"]
    #website1=details_json2["result"]["website"]
    #hwebsite0="http://"+website0
    #hwebsite1="http://"+website1



    #photo_id = search_json["results"][0]["photos"][0]["photo_reference"]
    #photo_link=photos_url+"?maxwidth=1600"+"&"+"photoreference="+photo_id+"&"+key
    
    photo_payload = {"key" : key, "maxwidth": 1600, "maxhight": 1600, "photoreference" : photo_id}
    photo_request = requests.get(photos_url, params=photo_payload)
    #final_pic=str(photo_request)
    
    final_pic=photos_url+ques+photo_width+amp+photo_ref+photo_id+amp+key_eq+"AIzaSyD8pgLKrEDnUYBoGVvpw0B4dT4qAyHaRXg"
    final_pic2=photos_url+ques+photo_width+amp+photo_ref+photo_id2+amp+key_eq+"AIzaSyD8pgLKrEDnUYBoGVvpw0B4dT4qAyHaRXg"

    #database filling
    db=psycopg2.connect(host="ec2-23-21-96-70.compute-1.amazonaws.com", dbname="d3cob9nu3ccmj5", user="enxlywbbucislp", password="fb2061f2d11f190a74770c77cc82cb676609952326cb5566236df137f3d182fb")
    cur=db.cursor()
    cur.execute("INSERT INTO enxlywbbucislp.FlowerChat(ID, TimeStamp) VALUES (ID, TimeStamp)")
    db.create_all()
    
    db.commit()
    cur.close()
    db.close()
    
    

    

    speech = "Here are the pictures of florists' work"


    print("Response:")
    print(speech)

    kik_message = [
        
        {
            "type": "picture",
            "picUrl": final_pic  

        },
        {
            "type": "text",
            "body": name_shop1+", phone: "+phone_shop1+", adress: "+form_add1
        },
        #{
         #   "type": "text",
          #  "body": "phone: " + phone_shop1
        #},
        #{
           # "type": "text",
            #"body": "address: "+form_add1
        #},
            
        #{
            #"type": "link"
            #"url": hwebsite0
        #},
        
        {
            "type": "picture",
            "picUrl": final_pic2
        },
        {
            "type": "text",
            "body": name_shop2+", phone: "+phone_shop2+", adress: "+form_add2
        },
        
            
        #{
            #"type": "link"
            #"url": hwebsite1
        #},
        {
            "type": "text",
            "body": "Please choose Florist A or Florist B",
            "keyboards":[
                {"type": "suggested",
                "responses": [
                     {
                         "type": "text",
                         "body": name_shop1
                     },
                     {
                         "type": "text",
                         "body": name_shop2
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