# Bedrock Data Summarizer
A Python script that takes a CSV file as an input, connects to AWS Lambda, and summarizes
the data using Google's Vertex AI (this is due to AWS blocking my Bedrock access, so I had to use Vertex)

## Setup
*Note: This assumes that you have already set up your AWS account and you have proper permissions for the user.*

1. **IAM Service User Role for Lambda**: You will need to create an IAM service user role for Lambda. You can do this in the AWS Console by doing the following steps:

> 1. Log in to the AWS Console with an account that has IAM Access and navigate to IAM.
> 2. Click on "Roles" in the left sidebar, and then click on "Create role" in the top right corner.
> 3. Select "AWS Service", and then open the dropdown and click "Lambda". Then click "Next".
> 4. On the "Permissions" page, you will need to attach the following policies:
> - `AmazonS3FullAccess`
> - `AWSLambda_FullAccess`
> - `AWSLambdaBasicExecutionRole`
> 5. Enter a name in the name field (e.g., "S3LambdaDataSum") and click "Create role".



2. **S3 Bucket Creation**: You will need to create an S3 bucket to store the CSV files that you want to summarize. You can do this in the AWS Console by doing the following steps:

> 1. Log in to the AWS Console with an account that has S3 Access and navigate to S3.
> 2. Click on "Create bucket" in the top right corner.
> 3. Enter a unique name for your bucket (e.g., "<your-initials>-data-summarizer-csv").
> 4. Leave the rest of the settings as default and click "Create bucket".
> 5. Repeat for the output bucket (e.g., "<your-initials>-data-summarizer-output").



3. **AWS Lambda** Creation: You will need to create up the AWS Lambda function. You can do this in the AWS Console by doing the following steps:

> 1. Log in to the AWS Console with an account that has Lambda Access & IAM Access and navigate to Lambda.
> 2. Click on "Create function" in the top right corner.
> 3. Select "Author from scratch", and enter a name for your function (e.g., "DataSummarizer"). For the runtime, select "Python 3.12".
> 4. Click on "Additional settings" in the "Custom settings" section, and toggle "Custom execution role".
> 5. Select "Use an existing role", and then select the IAM role you created in step 1 (e.g., "S3LambdaDataSum") and click "Save".
> 6. Leave everything else the same and click "Create function".



4. **AWS Lambda** Setup: You will need to upload the code, set environment variables, and add triggers to your Lambda function. You can do this in the AWS Console by doing the following steps:
> 1. Go to the GitHub Repository Releases page and download the latest lambda.zip file.
> 2. Uploading Code: In the Lambda function you just created, click "Update" and then "Update from a .zip file" and upload the lambda.zip file you downloaded from the GitHub Repository. Click "Save".
> 3. Adding S3 Trigger: In the Lambda function, click on "Add trigger". Click on "Select a source", scroll down and select "S3". Select the bucket you want as the trigger. Check the "Reverse invocation" notice and click "Add".
> 4. Setting Environment Variables: In the Lambda function, click on "Configuration" and click on "Environment variables" from the sidebar. Click "Edit" and add the following environment variables, then click "Save":
> - `SUMMARY_BUCKET`: The name of the S3 bucket you want to store the summaries in (e.g., "<your-initials>-data-summarizer-output").
> - `GOOGLE_CLOUD_PROJECT`: Your Google Cloud Project ID.
> - `GOOGLE_SERVICE_ACCOUNT_JSON`: The JSON string of your Google Service Account Key with access to Vertex AI. You can create a service account and download the key from the Google Cloud Console. Make sure to give the service account the necessary permissions for Vertex AI (e.g., "Vertex AI User" role). Note: Ask your administrator to get you the neccessary service key. This is not recommended for long-term use, but this is what worked for me.




## Usage

Clone the GitHub Repository and navigate to the project directory using the following commands:
```bash
git clone https://www.github.com/Bloomy52/bedrock-data-summarizer-py.git
cd bedrock-data-summarizer-py
```

Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

Run the Python script that runs the CLI:
```bash
python cli.py
```
or if your machine uses `python3` instead of `python`:
```bash
python3 cli.py
```

You will be prompted to enter the path of your CSV file. This CLI only takes CSV files as an input.

