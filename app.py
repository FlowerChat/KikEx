#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response


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
    

    speech = "Here are the examples of Florist A work"

    print("Response:")
    print(speech)

    kik_message = [
        
        {
            "type": "link",
            "url": "https://www.google.com/maps/contrib/105231077511067622688/photos/@-33.8712996,151.2043516,16z/data=!3m1!4b1!4m3!8m2!3m1!1e1&key=AIzaSyAb7Vnq1nSojwYd1TarHx_x6Gb4ti8bhVo"
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
