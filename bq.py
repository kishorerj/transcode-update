import argparse, sys, os, time, json
from datetime import datetime
from google.cloud import logging, bigquery

from google.cloud import storage


def create_bucket(bucket_name):
    client = storage.Client()
    bucket = storage.Bucket(bucket_name)
    client.create_bucket(bucket)

def update_job_status_in_bq(message):
    
    parsed_json1 = (json.loads(message))
    client = logging.Client()

    logger = client.logger("service_1")
    logger.log("message: " + message)
    
    job_id=parsed_json1["job"]["name"]
    status=parsed_json1["job"]["state"]
    error=""
    if "error" in parsed_json1:
        error=parsed_json1["job"]["error"]["message"]

    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    logger.log("job: " + job_id + "," + status)
    print("job: " + job_id + "," + status)
    project_id="kishorerjbloom"
    dataset_id="test_sample"
    table_id="trancoder_job_dtls"
    
    
    client = bigquery.Client()
    query_text = f"""
    UPDATE `{project_id}.{dataset_id}.{table_id}`
    SET status = "{status}", error_msg = "{error}", end_date = "{now}"
    WHERE job_id = "{job_id}"
    """
    query_job = client.query(query_text)

    # Wait for query job to finish.
    query_job.result()
    return 
