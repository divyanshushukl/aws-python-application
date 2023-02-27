import boto3
import os

# Specify the ARN of the role you want to assume, please delete once the testing is complete.
role_arn = 'arn:aws:iam::880096392120:policy/devops-assume-role'

# Create a new STS client and assume the role
sts_client = boto3.client('sts')
assumed_role = sts_client.assume_role(RoleArn=role_arn, RoleSessionName='my-session')

# Use the temporary credentials to create a new IAM client and list users
iam_client = boto3.client('iam',
    aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
    aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
    aws_session_token=assumed_role['Credentials']['SessionToken']
)
response = iam_client.list_users()
print(response['Users'])

# Use the temporary credentials to create a new IAM client and create a new user
new_username = 'my-new-user'
response = iam_client.create_user(UserName=new_username)
print('Created new IAM user:', new_username)

# Use the temporary credentials to create a new EC2 client and launch an instance
ec2_client = boto3.client('ec2',
    aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
    aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
    aws_session_token=assumed_role['Credentials']['SessionToken']
)
instance = ec2_client.run_instances(
    ImageId='ami-0c94855ba95c71c99',
    InstanceType='t2.micro',
    KeyName='my-key-pair',
    MinCount=1,
    MaxCount=1
)
print('Launched new EC2 instance:', instance['Instances'][0]['InstanceId'])
