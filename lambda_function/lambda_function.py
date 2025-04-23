import os
import boto3
import json
from faker import Faker
import pandas as pd

def lambda_handler(event, context):
    # Initialize Faker and other necessary libraries
    fake = Faker()
    
    # Extract the script and unique_id from the event
    script = event.get('script', '')
    unique_id = event.get('unique_id', 'default_unique_id')
    print(f"Received event: {event}")
    
    # Save the script to a temporary file
    script_file_path = f"/tmp/generated_script_{unique_id}.py"
    try:
        with open(script_file_path, 'w') as script_file:
            script_file.write(script)
        print(f"Script saved to {script_file_path}")
    except Exception as e:
        print(f"Error saving script: {e}")
        return {
            'statusCode': 500,
            'body': f"Error saving script: {e}"
        }
    
    # Define a scope dictionary to include necessary variables and imports
    scope = {
        'fake': fake,
        'pd': pd,
        'Faker': Faker,
        'os': os,
        'boto3': boto3
    }
    
    # Execute the script in the defined scope
    try:
        exec(open(script_file_path).read(), scope)
        print("Script executed successfully.")
        
        # Assuming the script generates a CSV file at /tmp/synthetic_data.csv
        csv_file_path = '/tmp/synthetic_data.csv'
        unique_filename = f"synthetic_data_{unique_id}.csv"
        
        # Upload to S3
        s3 = boto3.client('s3', endpoint_url=f"http://{os.environ['LOCALSTACK_HOSTNAME']}:{os.environ['EDGE_PORT']}")
        bucket_name = 'synthetic-data-bucket'
        s3.upload_file(csv_file_path, bucket_name, unique_filename)
        print(f"File uploaded to S3 bucket '{bucket_name}' successfully.")

        # Upload the script to S3
        script_s3_key = f"scripts/generated_script_{unique_id}.py"
        s3.upload_file(script_file_path, bucket_name, script_s3_key)
        print(f"Script uploaded to S3 bucket '{bucket_name}' successfully.")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'CSV file and script uploaded successfully.', 
                'csv_filename': unique_filename,
                'script_filename': script_s3_key
            })
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': f"Error occurred: {e}"
        }
