import boto3
import json

# Create SQS client
sqs = boto3.client('sqs')

queue_url = 'https://sqs.ap-southeast-1.amazonaws.com/331534983030/test' ##TO BE CHANGED BASED ON QUEUE CREATED

iot = boto3.client('iot-data') ## new iot rule to push to dynamodb

def alert(message):
    print("ALERTTTTTTTTTTTTTTTTTTTTT!!!!!!!!!")
    data = json.dumps(message)
    response = iot.publish(
             topic='/alert',
             payload=data
    ) 
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

    message_dict = json.loads(message.get('Body'))
    
    print("deviceParameter:", message_dict['deviceParameter'], "& deviceValue:", message_dict['deviceValue'])

    if message_dict['deviceParameter'] == 'Heart Rate' and (message_dict['deviceValue'] < 60 or message_dict['deviceValue'] > 100):
        alert(message)
    elif message_dict['deviceParameter'] == 'Oxygen Level' and message_dict['deviceValue'] < 94:
        alert(message)
    elif message_dict['deviceParameter'] == 'Blood Pressure' and (message_dict['deviceValue'] < 90 or message_dict['deviceValue'] > 140):
        alert(message)
    
