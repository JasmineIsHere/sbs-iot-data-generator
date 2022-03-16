import boto3

# Create SQS client
sqs = boto3.client('sqs')

queue_url = 'https://sqs.ap-southeast-1.amazonaws.com/331534983030/data-alert' ##to be changed

# Receive message from SQS queue
# sample message:
# {"deviceValue": 105, "deviceParameter": "Blood Pressure", "deviceId": "SBS05", "dateTime": "2022-03-16 19:47:14"}
while True:
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=20
    )

    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print('Received and deleted message: %s' % message)