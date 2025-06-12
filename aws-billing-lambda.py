import boto3

THRESHOLD = 50.0
SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:975050024946:awsbilling-satyam-sns'

def lambda_handler(event, context):
    sns = boto3.client('sns')

    # Simulate a billing value for testing
    simulated_billing = 75.32  #Assuming this as my AWS Bill

    print(f"[TEST] Simulated AWS Billing: ${simulated_billing:.2f}")


    if simulated_billing > THRESHOLD:
        message = f"[TEST ALERT] Simulated billing exceeded threshold. Amount: ${simulated_billing:.2f}"
        print("[TEST] Sending alert...")
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="AWS Billing Alert (Test)",
            Message=message
        )
    else:
        print("[TEST] Billing within threshold. No alert sent.")

