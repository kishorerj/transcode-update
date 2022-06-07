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
transcoder_notfns_cloudrun/app/bq.py /
@kishr4u
kishr4u updare end time
Latest commit 685672c on 8 May
 History
 1 contributor
47 lines (38 sloc)  1.68 KB
   
from google.cloud import bigquery
from datetime import datetime


def update_table():
    project_id="kishorerjbloom"
    dataset_id="test_sample"
    table="trancoder_job_dtls"
    table_id = project_id+ "." + dataset_id + "." + table
    client = bigquery.Client()
    query_text = f"""
    UPDATE `{project_id}.{dataset_id}.{table}`
    SET status = "FAILED"
    WHERE job_id="ABC3"
    """
    query_job = client.query(query_text)

    # Wait for query job to finish.
    query_job.result()


def insert_table(project, dataset, table, job_id, status, input_bucket_uri, output_bucket_uri, job_template):
    client = bigquery.Client()
    table_id = "kishorerjbloom.test_sample.trancoder_job_dtls"
    # datetime object containing current date and time
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
     
    rows_to_insert = [
        {u"job_id": job_id,  "status": status, u"start_date":now,u"end_date":now,
        u"input_media_uri": input_bucket_uri, u"output_transcoded_uri": output_bucket_uri,
        u"job_template": job_template}]
    errors = []
    #errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
    client = bigquery.Client()
    query_text = f"""
    INSERT {project}.{dataset}.{table} (job_id, status, start_date, end_date, input_media_uri, output_transcoded_uri, job_template)  
    VALUES ('{job_id}', '{status}','{now}', '{now}', '{input_bucket_uri}', '{output_bucket_uri}', '{job_template}')
    """
    query_job = client.query(query_text)

    query_job.result()
    

if __name__ == "__main__":
    insert_table("kishorerjbloom", "test_sample","trancoder_job_dtls", "ABC3", "DONE", "input", "output", "templ")
    update_table()
    print("main hello")
