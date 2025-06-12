import boto3
from datetime import datetime, timezone

def lambda_handler(event, context):
    bucket_name = 'satyam-s3-bucket-lambda'
    days_old = 30

    s3 = boto3.client('s3')
    now = datetime.now(timezone.utc)
    deleted_files = []

    # List files in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']

            # Get metadata
            metadata = s3.head_object(Bucket=bucket_name, Key=key).get('Metadata', {})
            creation_date_str = metadata.get('creation-date')

            if creation_date_str:
                creation_date = datetime.strptime(creation_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                age = (now - creation_date).days

                if age > days_old:
                    s3.delete_object(Bucket=bucket_name, Key=key)
                    deleted_files.append(key)

    print("Deleted files:")
    for file in deleted_files:
        print(f"- {file}")

    return {
        'statusCode': 200,
        'body': f"Deleted {len(deleted_files)} files"
    }

