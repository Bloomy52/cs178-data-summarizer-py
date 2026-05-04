import boto3
import os
import json
import csv
import creds
import hashlib
from io import BytesIO

# This is the lambda Python file which is executed by Lambda

def lambda_handler(event, context):
    """
    Entry point for the Lambda function.

    AWS calls this automatically when an S3 object-created event fires.
    The 'event' dict contains details about what was uploaded.
    """

    # ── Step 1: Extract the bucket name and filename from the trigger event ───
    # When S3 triggers Lambda, the event contains a 'Records' list.
    # Each record describes one file that was uploaded.
    s3 = boto3.client("s3")
    record = event["Records"][0]
    source_bucket = record["s3"]["bucket"]["name"]
    filename = record["s3"]["object"]["key"]

    print(f"Triggered by upload: s3://{source_bucket}/{filename}")

    # ── Step 2: Open the prompt.txt file ──────────────
    with open("prompt.txt", "r") as infile:
       prompt = infile.read()

    # ── Step 3: Open the csv file from S3 and upload to Bedrock ──────────────
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Open the Uploaded CSV file
    response = bedrock.converse(
        modelId="global.amazon.nova-2-lite-v1:0",
        messages=[{
            "role": "user",
            "content": [
                {"document": {
                    "format": "csv",
                    "name": filename,
                    "source": {"s3": f"s3://{source_bucket}/{filename}"}
                }
                },
                {"text": prompt}
            ]
        }]
    )

    # ── Step 4: Write the summary to a new text file  ─────────────
    output = response["output"]["message"]["content"][0]["text"]

    with open(f"./summary_temps/{filename}.txt", "w") as outfile:
        outfile.write(output)


    # ── Step 5: Save the txt summary back into a BytesIO buffer ─────────────
    buffer = BytesIO()
    file_format = "txt"
    txt_filename = f"{filename}.txt"


    # ── Step 6: Upload the result to the processed bucket ─────────────────────
    s3.put_object(
        Bucket=creds.S3_SUMMARY_BUCKET,
        Key=txt_filename,           # same filename, different bucket
        Body=buffer,
        ContentType=f"txt/{file_format.lower}",
    )

    print(f"Processed image saved to: s3://{creds.S3_SUMMARY_BUCKET}/{txt_filename}")

    return {
        "statusCode": 200,
        "body": f"Summarized {filename} and saved to {creds.S3_SUMMARY_BUCKET}"
    }



