import boto3
import os
import creds
import time

# This is the initial CLI which uploads the file to S3 and takes the summary output from
# Amazon Bedrock and displays it to the user.

def upload_to_s3(filepath, bucket, key):
    """
    Uploads the CSV file to the CSV S3 bucket
    :param filepath: the filepath to the CSV file
    :param bucket: Bucket name from the creds.py file
    :param key: the filename of the CSV to be uploaded
    :return: a Boolean which returns True if file was uploaded successfully.
    """
    s3 = boto3.client('s3', region_name=creds.AWS_REGION)
    s3.upload_file(filepath, bucket, key)

    # TODO: Finish adding the code to upload the CSV to S3
    # ...
    return None


def display_bedrock_summary(bucket, filename):
    """
    Displays the summary of the CSV file from Bedrock
    :param bucket: the summary bucket name
    :param filename: the filename of the txt file with the summary data
    :return: None. Just displays the summary data
    """

    s3 = boto3.client('s3', region_name=creds.AWS_REGION)

    s3.download_file(bucket, f"{filename}.txt", f'./summary_downloads/{filename}.txt')

    with open(f"./summaries/{filename}.txt", 'r') as infile:
        summary = infile.read()

    print(summary)


# Main Function:
def main():
    # Main Interactive Filename Loop:
    # Get input file
    while True:
        filepath = input("\nEnter the path to your CSV file: ").strip()

        # Remove quotes if user wrapped path in quotes
        input_file = filepath.strip('"\'')

        if not os.path.exists(input_file):
            print(f"Error: File '{input_file}' not found.  Please try again.")
            continue

        if not input_file.lower().endswith('.csv'):
            print("Warning: file extension is not .csv. Continue anyway? (y/n)")
            if input().lower() != 'y':
                continue

        break

    filename = os.path.basename(input_file)
    upload_to_s3(input_file, creds.S3_CSV_BUCKET, filename)
    time.sleep(30)
    display_bedrock_summary(creds.S3_SUMMARY_BUCKET, filename)


    return None



# File Start
if __name__ == "__main__":
    main()
