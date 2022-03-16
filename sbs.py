# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
    
# Script to generate simulated IoT device parameters data

import json
import random
import datetime
import boto3
import time

deviceNames = ['SBS01', 'SBS02', 'SBS03', 'SBS04', 'SBS05']

iot = boto3.client('iot-data')

# generate Heart Rate values
def getHeartRateValues():
    data = {}
    healthyHR = random.randint(60,100)
    unhealthyHR = random.randint(40,120)

    data['deviceValue'] = random.choices([healthyHR, unhealthyHR],[0.8, 0.2])[0]
    data['deviceParameter'] = 'Heart Rate'
    data['deviceId'] = random.choice(deviceNames)
    data['dateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return data

# generate Oxygen Level values
def getOxygenLevelValues():
    data = {}
    healthyO2 = random.randint(94,100)
    unhealthyO2 = random.randint(90,100)

    data['deviceValue'] = random.choices([healthyO2, unhealthyO2],[0.8, 0.2])[0]
    data['deviceParameter'] = 'Oxygen Level'
    data['deviceId'] = random.choice(deviceNames)
    data['dateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return data

# generate Blood Pressure values
def getBloodPressureValues():
    data = {}
    healthyBP = random.randint(90,120)
    unhealthyBP = random.randint(80,150)

    data['deviceValue'] = random.choices([healthyBP, unhealthyBP],[0.8, 0.2])[0]
    data['deviceParameter'] = 'Blood Pressure'
    data['deviceId'] = random.choice(deviceNames)
    data['dateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return data

# Generate each parameter's data input in varying proportions
LIMIT = 500 #iot output limit - just to not exceed SQS free-tier (1 million requests per month)
count = 0
while count < LIMIT:
    count += 1
    time.sleep(1)
    rnd = random.random()
    if (0 <= rnd < 0.30):
        data = json.dumps(getHeartRateValues())
        print (data)
        response = iot.publish(
             topic='/sbs/devicedata/heart',
             payload=data
        ) 
    elif (0.30<= rnd < 0.60):
        data = json.dumps(getOxygenLevelValues())
        print (data)
        response = iot.publish(
             topic='/sbs/devicedata/oxygen',
             payload=data
        )
    else:
        data = json.dumps(getBloodPressureValues())
        print (data)
        response = iot.publish(
             topic='/sbs/devicedata/bp',
             payload=data
        )
