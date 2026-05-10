import boto3
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from io import BytesIO

# This is the lambda Python file which is executed by Lambda

def lambda_handler(event, context):
    """
    Entry point for the Lambda function.

    AWS calls this automatically when an S3 object-created event fires.
    The 'event' dict contains details about what was uploaded.
    """
    # Load Environment Variables
    load_dotenv()
    AWS_REGION = os.environ["AWS_REGION"]
    SUMMARY_BUCKET = os.environ["SUMMARY_BUCKET"]
    PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]

    MODEL_ID = "gemini-3-flash-preview"

    LOCATION = "global"

    client = genai.Client(enterprise=True, project=PROJECT_ID, location=LOCATION)

    # ── Step 1: Extract the bucket name and filename from the trigger event ───
    # When S3 triggers Lambda, the event contains a 'Records' list.
    # Each record describes one file that was uploaded.
    s3 = boto3.client("s3")
    record = event["Records"][0]
    source_bucket = record["s3"]["bucket"]["name"]
    filename = record["s3"]["object"]["key"]

    print(f"Triggered by upload: s3://{source_bucket}/{filename}")

    # ── Step 2: Create the prompt for Bedrock: ──────────────
    # Prompt was adapted from the official documentation
    # Use this to clearly define the task and job needed by the model
    task_summary = f"""
    ## Task Summary:
    {{Review the attached CSV and summarize what the data covers, including anything notable or unusual.}}
    """

    # Use this to provide contextual information related to the task
    context_information = f"""
    ## Context Information:
    - {{Standard CSV format with headers in the first row}}
    - {{Columns may include numbers, text, or dates}}
    """

    # Use this to provide any model instructions that you want model to adhere to
    model_instructions = f"""
    ## Model Instructions:
    - {{Explain what each column represents and flag anything out of the ordinary}}
    - {{Base all observations only on the data provided}}
    """

    # Use this to provide response style and formatting guidance
    response_style = f"""
    ## Response style and format requirements:
    - {{Write as if explaining the data to a coworker}}
    - {{Use three sections: overview, column breakdown, and key takeaways}}
    - {{Limit the response to 300 words or less}}
    - {{Use Proper Markdown Formatting, including headings and bullet points where appropriate}}
    """

    # Concatenate to final prompt
    final_prompt = f"""{task_summary}
    {context_information}
    {model_instructions}
    {response_style}"""

    # ── Step 3: Open the csv file from S3 and upload to Bedrock ──────────────

    # Open the Uploaded CSV file
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[
            types.Part.from_uri(
                file_uri="s3://{source_bucket}/{filename}",
                mime_type="application/csv",
            ),
            final_prompt,
        ]
    )

    # ── Step 4: Write the summary to a new text file  ─────────────
    output = response.text

    with open(f"./summary_temps/{filename}.txt", "w") as outfile:
        outfile.write(output)


    # ── Step 5: Save the txt summary back into a BytesIO buffer ─────────────
    buffer = BytesIO()
    file_format = "txt"
    txt_filename = f"{filename}.txt"


    # ── Step 6: Upload the result to the processed bucket ─────────────────────
    s3.put_object(
        Bucket=SUMMARY_BUCKET,
        Key=txt_filename,           # same filename, different bucket
        Body=buffer,
        ContentType=f"txt/{file_format.lower}",
    )

    print(f"Summary saved to: s3://{SUMMARY_BUCKET}/{txt_filename}")

    return {
        "statusCode": 200,
        "body": f"Summarized {filename} and saved to {SUMMARY_BUCKET}"
    }