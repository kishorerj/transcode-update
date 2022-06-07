Skip to content
Search or jump to…
Pull requests
Issues
Marketplace
Explore
 
@kishr4u 
kishr4u
/
transcoder_notfns_cloudrun
Public
Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
transcoder_notfns_cloudrun/app/app.py /
@kishr4u
kishr4u update notfn status in bq
Latest commit c778c49 on 7 May
 History
 1 contributor
51 lines (38 sloc)  1.26 KB
   
import logging as pythonlogging
import os
import base64
import update_job_status
from google.cloud import logging
from flask import Flask, request
from secure import require_apikey


app = Flask(__name__)


@app.route('/health')
def health():
    return 'It is alive!\n'


@app.route('/hello')
@require_apikey
def hello():
    return {'hello': 'world'}

@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]
    
    client = logging.Client()
    logger = client.logger("service_1")
    logger.log(pubsub_message)
    
    name = "World"
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        name = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
    logger.log(name)
   
    update_job_status.update_job_status_in_bq(name)
    return ("DONE", 204)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
© 2022 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
Loading complete
