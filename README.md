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

Create the `creds.py` file in the project directory. Add the following variables to the `creds.py` file.
```python
# creds.py
AWS_REGION = "Your AWS Region (e.g., us-east-1)"
S3_CSV_BUCKET = "Your S3 bucket name for CSV files (e.g., <your-initials>-data-summarizer-csv)"
S3_SUMMARY_BUCKET = "Your S3 bucket name for summaries (e.g., <your-initials>-data-summarizer-output)"
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
*Note: You cannot have spaces in the CSV file name. The program will fail otherwise.*

## Example:
For this example, we will use the `CTA_RedLine_Ridership_Addison-NorthMain-WrigleyField.csv` file that is included in the `example` folder.*
1. Run the CLI:
```bash
python cli.py
```
2. Paste the path of the CSV file:
```text
example/CTA_RedLine_Ridership_Addison-NorthMain-WrigleyField.csv
```
3. 30 seconds later, the summary will be printed in the console and a text file with the summary will be output to the `summaries` folder. 
4. The output below is from when I ran it on the example CSV file, your output may differ. You can find this exact output in the `example` folder.:
```text
Overview

This dataset provides a daily log of transit usage at a single location, the Addison-North Main station, identified by ID 41420. The records span over 25 years, beginning in January 2001 and continuing through February 2026. The data tracks volume fluctuations across different day types, revealing clear seasonal cycles and significant one-off events that impacted how many people used this specific stop.

Column Breakdown

- station_id: A unique five-digit numeric code (41420) that identifies the specific transit station.
- stationname: The descriptive name of the stop, which is "Addison-North Main" for the entire set.
- date: The specific calendar day for the ridership count, provided in MM/DD/YYYY format.
- daytype: A single-letter code representing the schedule type. "W" indicates typical weekdays, "A" represents Saturdays, and "U" stands for Sundays or holidays.
- rides: The total count of passenger boardings recorded for that day.

Key Takeaways

- Volatility and Event Spikes: Daily ridership is highly variable. While a standard weekday often sees between 5,000 and 7,000 rides, there are extreme surges where volume exceeds 20,000 or even 30,000. Notably, on October 29, 2016, ridership peaked at 33,615. This specific surge corresponds to the Chicago Cubs' World Series run, as this station serves Wrigley Field. Similar high-volume patterns appear every year during the spring and summer months, likely tied to the baseball season.

- The 2020 Collapse: There is a massive, sudden decline starting in mid-March 2020. Volume dropped from 5,925 on March 9 to just 512 by March 24. This reflects the impact of the COVID-19 pandemic. Unlike previous years where ridership recovered seasonally, the post-2020 numbers remain suppressed for an extended period, only beginning to show a slow, partial climb toward older averages by 2024 and 2025.

- Day Type Patterns: Historically, weekdays (W) show the highest consistent traffic, followed by Saturdays (A), with Sundays (U) typically being the quietest. However, during major events or holidays, these patterns invert. For example, some Sundays during peak season see higher traffic than winter weekdays.

- Data Anomalies: There are several instances of unusually low numbers that suggest station closures or service interruptions. For instance, on June 13, 2001, only 128 rides were recorded, and on March 30, 2019, the count dropped to 40, which are both significant outliers compared to surrounding dates.

- Long-term Trends: Before 2020, the station saw a gradual increase in baseline ridership over the decades. The data recorded for 2025 and early 2026 suggests the station is still in a phase of re-stabilizing its volume following the multi-year disruption that began in 2020.
```

***
*Example data was obtained from the Chicago Data Portal: https://data.cityofchicago.org. You can find the original dataset [here](https://data.cityofchicago.org/Transportation/CTA-Ridership-L-Station-Entries-Daily-Totals/5neh-572f/about_data).
