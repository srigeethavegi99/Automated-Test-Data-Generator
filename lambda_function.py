import os
import json
import boto3

def lambda_handler(event, context):
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

    # Return success response for script handling
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Script saved successfully.',
            'script_file_path': script_file_path
        })
    }
