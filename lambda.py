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
    record = event["Records"][0]
    source_bucket = record["s3"]["bucket"]["name"]
    filename = record["s3"]["object"]["key"]

    print(f"Triggered by upload: s3://{source_bucket}/{filename}")

    # ── Step 2: Download the uploaded image from S3 into memory ──────────────
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=source_bucket, Key=filename)
    csv_data = response["Body"].read()



    # ── Step 4: Save the txt summary back into a BytesIO buffer ─────────────
    buffer = BytesIO()
    file_format = "txt"


    # ── Step 5: Upload the result to the processed bucket ─────────────────────
    s3.put_object(
        Bucket=creds.S3_SUMMARY_BUCKET,
        Key=filename,           # same filename, different bucket
        Body=buffer,
        ContentType=f"txt/{file_format.lower}",
    )

    print(f"Processed image saved to: s3://{creds.S3_SUMMARY_BUCKET}/{filename}")

    return {
        "statusCode": 200,
        "body": f"Flipped {filename} and saved to {creds.S3_SUMMARY_BUCKET}"
    }



