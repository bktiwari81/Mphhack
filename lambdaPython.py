import boto3

REGION = 'us-west-2' # region to launch instance.
AMI = 'ami-a0cfeed8'
    # matching region/setup amazon linux ami, as per:
    # https://aws.amazon.com/amazon-linux-ami/
INSTANCE_TYPE = 'm3.medium' # instance type to launch.

EC2 = boto3.client('ec2', region_name=REGION)

def lambda_to_ec2(event, context):
    """ Lambda handler taking [message] and creating a httpd instance with an echo. """
    message = event['message']

    # bash script to run:
    #  - update and install httpd (a webserver)
    #  - start the webserver
    #  - create a webpage with the provided message.
    #  - set to shutdown the instance in 10 minutes.
    init_script = """#!/bin/bash
        yum update -y
        yum install -y httpd24
        yum install git
        yum install nodejs
        git clone https://github.com/khandelwal14/healthcheck-service.git
        npm install claudia-api-builder --save
        npm install -g claudia
        claudia create --timeout 10 --region us-west-2 --api-module src/app 
        npm install
        npm run dev
        service httpd start
        chkconfig httpd on
        echo """ + message + """ > /var/www/html/index.html
        shutdown -h +10"""

    print ("Running script:")
    print (init_script)

    instance = EC2.run_instances(
        ImageId=AMI,
        InstanceType=INSTANCE_TYPE,
        MinCount=1, # required by boto, even though it's kinda obvious.
        MaxCount=1,
        InstanceInitiatedShutdownBehavior='terminate', # make shutdown in script terminate ec2
        UserData=init_script # file to run on instance init.
    )

    print ("New instance created.")
    instance_id = instance['Instances'][0]['InstanceId']
    print (instance_id)

    return instance_id
