import boto3

def lambda_handler(event, context):
    # TODO implement
    ec2=boto3.client('ec2')

    #FDescribing the all Ec2 Instance & Fetching tags and values info
    instances = ec2.describe_instances()

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            
            #To more filteration added LaunchedBy tag
            if tags.get('LaunchedBy') == 'Satyam':
                action = tags.get('Action')
                
                #Checking and Starting instance if it is in stopped state
                if action == 'Auto-Start' and state == 'stopped':
                    ec2.start_instances(InstanceIds=[instance_id])
                    print(f"Started instance {instance_id}")
                
                #Checking and Stopping instance if it is in running state
                elif action == 'Auto-Stop' and state == 'running':
                    ec2.stop_instances(InstanceIds=[instance_id])
                    print(f"Stopped instance {instance_id}")

    return {"status": "Done"}

