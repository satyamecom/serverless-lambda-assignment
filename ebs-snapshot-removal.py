import boto3
from datetime import datetime, timedelta

ec2 = boto3.client('ec2')
VOLUME_ID = 'vol-0e9fd4e2ff7ad0515' #Used my Ec2 instance volume id
RETENTION_DAYS = 30

def lambda_handler(event, context):
    old_date = datetime.utcnow() - timedelta(days=RETENTION_DAYS)

# Get all snapshots for this volume
    snapshots = ec2.describe_snapshots(
        Filters=[{'Name': 'volume-id', 'Values': [VOLUME_ID]}],
        OwnerIds=['self']
    )['Snapshots']

    for snapshot in snapshots:
        snapshot_time = snapshot['StartTime'].replace(tzinfo=None)
        if snapshot_time < old_date:
            ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            print(f"Deleted snapshot: {snapshot['SnapshotId']} (Date: {snapshot_time})")

    return {
        'statusCode': 200,
        'body': 'Old snapshots deleted successfully.'
    }

