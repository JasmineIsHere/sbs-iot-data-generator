# Table of Contents
- [AWS IoT Simple Beer Service](#aws-iot-simple-beer-service)
- [AWS IoT Rule](#aws-iot-rule)
- [AWS IoT Rule to Lambda to SNS](#aws-iot-rule-to-lambda-to-sns)

# AWS IoT Simple Beer Service
## Sample Data Generator for AWS IoT Simple Beer Service

This is the code repository for sample code to locally generate IoT device data similar to what is generated by the [AWS Simple Beer Service](https://github.com/awslabs/simplebeerservice) devices, and feed it to AWS IoT service.

### Pre-requisites

* Amazon Web Services account
* [AWS Command Line Interface (CLI)](https://aws.amazon.com/cli/)
* Python
* boto3

### Script Details

The script generates random values (within a reasonable range) for each of the three parameters- Heart Rate, Oxygen Level, and Blood Pressure, with 20% chance of an abnormal reading appearing randomly (to signal an alert for the doctors). 

This script was originally taken from [aws-samples](https://github.com/aws-samples/sbs-iot-data-generator).

### Running Example

`$ python sbs.py` 

## Run the script on Amazon EC2 Instance

To run it from an Amazon EC2 instance. Follow these steps:

1. Create an IAM role with a policy that gives access to IoT (example: AWSIoTFullAccess)
2. Launch a new EC2 instance and assign it the IoT IAM role at launch
3. Login to the EC2 instance and change to root user `sudo su`
4. Set your default region and output format in `aws configure`
> Access Key ID: \<your access key> <br>
Secret Access Key: \<your secret access key> <br>
Default region: ap-southeast-1 <br>
Default output format: json
5. Upload `sbs.py` file to EC2, or `nano sbs.py`, copy the entire script, save and exit
6. ~~Make sure you have boto3 installed. If not, type `pip install boto3`~~
7. ~~Run `python sbs.py`~~
8. Check if you have pip with `pip --version`
    else: `python -m ensurepip --upgrade`
9. Use pip to install Boto3: `pip install install boto3`
10. Run `sbs.py` from ec2: `python3 run python sbs.py`

## Retrieve data using IoT Rules:

1. Go to AWS IoT Rules and create a new rule
2. Include rule query statement: `SELECT * FROM '/sbs/devicedata/#'`
> keep the topic filter (/sbs/devicedata/#') the same unless you change it in the sbs.py file
3. Select what you want to do with the data (action):
> E.g. Send a message to an SQS queue (but you will have to create the queue in advance)

# AWS SQS & IoT Rule

# AWS IoT Rule to Lambda to SNS
## lambda_from_iot_to_sns.py 

The `lambda_from_iot_to_sns.py` file contains the code to create a AWS Lambda service is triggered by an IoT rule and sends a message to a SNS service.

To test this on your own AWS account, you will need the following service set up:
- AWS IoT Rule
- AWS Lambda
- AWS SNS

### AWS IoT Rule

IoT Rule is used to read MQTT messages hence when creating a new IoT rule, you need to specify the source of your messages (the topic you are subscribing to) in the *Rule Query Statement* and what you want to do with the message with *Actions*.

<image></image>
*In this case, I have my IoT Rule subsribed to all the messages from the `/alert` topic and it will send a message to Lambda when the rule is triggered*


To test your IoT Rule is working properly, you can make use of the MQTT test client in AWS IoT Core to subscribe/publish to a topic.
<image></image>

### AWS Lambda
The Lambda service will execute upon a trigger. In this case, the trigger is the AWS IoT rule. When creating a new Lmabda function, use the runtime `Python 3.9` and paste the `lambda_from_iot_to_sns.py` into the Code Source.
Remember to always "Deploy" any changes to the code in order to save the latest version. 
<image><image>
<br>
You may test the service directly by creating a new test event and passing in the sample JSON input into the Event JSON.
<image><image>
