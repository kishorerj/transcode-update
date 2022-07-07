   
import logging as pythonlogging
import os
import base64
import bq
from google.cloud import logging
from flask import Flask, request


app = Flask(__name__)


@app.route('/test')
def test():
    return 'I am alive!'


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
   
    bq.update_job_status_in_bq(name)
    return ("DONE", 204)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
