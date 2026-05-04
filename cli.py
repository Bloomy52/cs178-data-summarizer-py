import boto3
import os
import creds
import csv

# This is the initial CLI which uploads the file to S3 and takes the summary output from
# Amazon Bedrock and displays it to the user.

def upload_to_s3(bucket, key):
    """
    Uploads the CSV file to the CSV S3 bucket
    :param filename: filename of the CSV file to be uploaded
    :param bucket: Bucket name from the creds.py file
    :param key: the filename of the CSV to be uploaded
    :return: a Boolean which returns True if file was uploaded successfully.
    """
    s3 = boto3.resource('s3', region_name=creds.AWS_REGION)
    csv_bucket = s3.Bucket(bucket)

    # TODO: Finish adding the code to upload the CSV to S3
    # ...
    return None


def display_bedrock_summary(bucket):
    """
    Displays the summary of the CSV file from Bedrock
    :param bucket: the summary bucket name
    :param key: the filename of the txt file with the summary data
    :return: None. Just displays the summary data
    """

    s3 = boto3.resource('s3', region_name=creds.AWS_REGION)
    summary_bucket = s3.Bucket(bucket)
    response = s3.get_object(Bucket=summary_bucket, Key=txt_filename)
    summary_data = response["Body"].read()




# Main Function:
def main():
    # Main Interactive Filename Loop:
    # Get input file
    while True:
        input_file = input("\nEnter the path to your CSV file: ").strip()

        # Remove quotes if user wrapped path in quotes
        input_file = input_file.strip('"\'')

        if not os.path.exists(input_file):
            print(f"✗ Error: File '{input_file}' not found.  Please try again.")
            continue

        if not input_file.lower().endswith(('.csv')):
            print("Warning: file extension is not .csv. Continue anyway? (y/n)")
            if input().lower() != 'y':
                continue

        break

        upload_to_s3(creds.S3_CSV_BUCKET, input_file)



    return None



# File Start
if __name__ == "__main__":
    main()
