# What is this repo?

This repo is the code base used for the talk '*Live Coding Cloud Apps with CDK
(infrastructure as code)*'.

Following this README.md will guide you to create your first cloud application
using [AWS CDK](https://github.com/aws/aws-cdk). CDK is a development framework
that will help you to write infrastructure as code using your favorite language
(Typescript, Python, Javascript, Java, C# and others), for more information
about CDK take a look at
[this](https://docs.aws.amazon.com/cdk/latest/guide/home.html).

The result of this live coding session can be find at the '*/cloud-app-cdk/*'
directory. **This is not production ready code** and probably not the best
styled code but it works when it comes to understand how to develop with CDK.

# Thanks
It is inspired by
[cdkworkshop.com](https://cdkworkshop.com/),
[@darkosubotica](https://twitter.com/darkosubotica)
[talks](https://www.youtube.com/channel/UCV_UAKu9-r39cEEXPj_xWfw),
[cdkday.com](https://www.cdkday.com/),
[awsome-cdk](https://github.com/kolomied/awesome-cdk) repository and
[cdk.dev](https://cdk.dev).
I would like to thank all of them which provided a lot of resources that
allowed me to learn the basis about CDK and bring it to my collegues.

# Let's get started!
This document is intended to guide you in the process of building your first
cloud application with CDK using Python so it is divided in a few sections
where you will do something neecessary for the next section, this is better do
not try to hurry up and avoid a section since you could regret it in the
following ones.

Note: it is important to know that you need a AWS account with environment
variables set with AWS credentials. Check it out
[awsume](https://github.com/trek10inc/awsume).

## Install CDK toolkit
### MacOS
Pre-requisites: [brew](https://brew.sh/)
```sh
~ $ brew install node
~ $ npm i -g aws-cdk
~ $ cdk --version
```
### Linux (Ubuntu 18.04 and 16.04)
```sh
~ $ sudo apt install nodejs
~ $ npm install -g aws-cdk
~ $ cdk --version
```

## Init app && prepare virtualenv
Tipically CDK applications are developed in a local directory:
```sh
~ $ mkdir cloud-app-cdk
~ $ cd cloud-app-cdk
```
CDK toolkit helps you to initialize the app directory creating code base for
you where you can start coding immediately.
```sh
~/cloud-app-cdk $ cdk init --language python
..
.
Executing Creating virtualenv...
```
As you probably observed CDK toolkit created a virtualenv for you so let's
activate it. It is something you should do everytime you develop you
application.
```sh
~/cloud-app-cdk $ source .venv/bin/activate
```
Before starting the actual CDK workflow it is necessary to install some core
modules:
```sh
(.venv) ~/cloud-app-cdk $ pip install -r requirements.txt
```
## CDK app structure
Well, first of all let's check what the CDK toolkit created for you.
```
README.md
app.py                                <--- CDK toolkit entry point
cdk.json                              <--- CDK toolkit configuration stuff
cloud_app_cdk/                        <--- cloud application code
requirements.txt
setup.py
source.bat
```
Your application's stack will be created in a very special file called
'*cloud_app_cdk/cloud_app_cdk_stack.py*'. More complex applications could be
composed by more than one stack but in this case just one stack is needed.

# Bootstraping your AWS account
CDK toolkit needs some AWS resources that will be used to deploy your
application.
```sh
(.venv) ~/cloud-app-cdk $ cdk bootstrap
```
This will create a new AWS CloudFormation stack in your AWS account. It is only
necessary to be run one time. Mainly this is a bucket to store artifacts.

# Let's deploy something
At this point you will learn how to deploy something into your AWS account,
let's start with a lambda function that will be useful in further phases.

## AWS Lambda construct library
In order to be able to do it you need to install the Python module that will
make the AWS Lambda construct library available which will allow you to use the
AWS Lambda constructs in your CDK code.

```sh
(.venv) ~/cloud-app-cdk $ pip install aws-cdk.aws-lambda
```

Lambda code needs to be located in the CDK application root directory as follow:
```sh
(.venv) ~/cloud-app-cdk $ mkdir lambda
```

## Hello World lambda
### Code
Edit the following file where the lambda's code will be written:
```sh
(.venv) ~/cloud-app-cdk $ vim lambda/hello.py
```
```python
import json

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello, CDK! You have hit {}\n'.format(event['path'])
    }
```

### AWS resource
Now you are ready to create a new resource using the AWS Lambda construct
library. Just edit the '*cloud_app_cdk/cloud_app_cdk_stack.py*' file.

Import the AWS Lambda python module:
```python
from aws_cdk import aws_lambda as _lambda
```
Create a new AWS Lambda resource like this:
```python
class CloudAppCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Hello lambda
        hello_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='hello.handler',
            timeout=core.Duration.seconds(30)
        )
```

### Deploy
Now it's time to deploy your CDK application for the first time.
```sh
(.venv) ~/cloud-app-cdk $ cdk deploy
```
You can check you AWS account at CloudFormation service and you will notice
a new CloudFormation stack is created.

# API Gateway
A typical resource necessary in cloud application is an API, this resource
usually requires a lot of lines of code when you are coding AWS CloudFormation,
however let's see how it looks in CDK.

## Install API Gateway construct library
Again, you need to install the python package that contains the AWS APIGateway
construct library. It is always you need to do when using a construct library.
```sh
(.venv) ~/cloud-app-cdk $ pip install aws-cdk.aws-apigateway
```

## Add API Gateway resource
```python
from aws_cdk import aws_apigateway as apigw
..
..
        # Hello lambda resource
        ..
        ..

        # API Gateway
        cloud_app_apigw = apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_lambda,
        )
```

## Diff
Before trying to deploy again the changes let's see what is different between
the local cdk application and the one deployed.
```sh
(.venv) ~/cloud-app-cdk $ cdk diff
```

## Deploy
It looks good and obviously new resources are going to be deployed as shown in
the '*cdk diff*' before.
```sh
(.venv) ~/cloud-app-cdk $ cdk deploy cloud-app-cdk
```
![New API gateway resources](./assets/apigw_resources.png)
As you see it will add twelve new resources.

## Test
```
Outputs:
cloud-app-cdk.Endpoint8024A810 = https://jmedoa58w2.execute-api.eu-west-1.amazonaws.com/pro

(.venv) ~/cloud-app-cdk $ curl https://jmedoa58w2.execute-api.eu-west-1.amazonaws.com/prod/
Hello, CDK! You have hit /
```

# DynamoDB & Writing lambda & API Gateway Integration
```sh
(.venv) ~/cloud-app-cdk $ pip install aws-cdk.aws-dynamodb
```

```python
from aws_cdk import aws_dynamodb as dynamodb
..
..
        # Dynamodb
        table = dynamodb.Table(
            self,
            'messages',
            partition_key=dynamodb.Attribute(
                name='author',
                type=dynamodb.AttributeType.STRING
            ),
            table_name='messages'
        )
..
..
        # Message lambda
        message_lambda = _lambda.Function(
            self, 'MessageHandler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='message.handler',
            timeout=core.Duration.seconds(30)
        )
        cloud_app_apigw_integration = apigw.LambdaIntegration(message_lambda)
        api_message = cloud_app_apigw.root.add_resource("message")
        api_message.add_method("POST", cloud_app_apigw_integration)
```

Message lambda code (message.py):
```python
import os
import json
import boto3

def handler(event, context):
    table = os.environ.get('table')
    dynamodb = boto3.client('dynamodb')

    item = {
            "author":{'S':event["queryStringParameters"]["author"]},
            "message":{'S':event["queryStringParameters"]["message"]}
            }

    
    response = dynamodb.put_item(TableName=table,
            Item=item
            )

    message = 'Status of the write to DynamoDB {}!'.format(response)  
    return {
        "statusCode": 200,
        "body": json.dumps(message)
    }
```

Environmnet variables:
```python
        # Message lambda
        message_lambda = _lambda.Function(
            self, 'MessageHandler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='message.handler',
            timeout=core.Duration.seconds(30),
            environment={'table': 'messages'}   <----------
        )
```

# Reading lambda
```python
        # Read lambda
        read_lambda = _lambda.Function(
            self, 'ReadHandler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='read.handler',
            timeout=core.Duration.seconds(30),
            environment={'table': 'messages'}
        )

        cloud_app_apigw_integration = apigw.LambdaIntegration(read_lambda)
        api_message = cloud_app_apigw.root.add_resource("read")
        api_message.add_method("GET", cloud_app_apigw_integration)
```
CFN Resources
```python
        # L1 resources to add 'description'
        cfn_read_lambda = read_lambda.node.default_child
        cfn_read_lambda.description = "Messages reading lambda"
```
Read lambda code (read.py):
```python
import os
import json
import boto3

def handler(event, context):
    table = os.environ.get('table')
    dynamodb = boto3.client('dynamodb')

    key = {
            "author":{'S':event["queryStringParameters"]["author"]}
            }

    response = dynamodb.get_item(TableName=table,
            Key=key
            )

    return {
        "statusCode": 200,
        "body": json.dumps(response["Item"])
    }
```
# Permissions
```python
        # Permissions
        table.grant_read_data(read_lambda)
        table.grant_write_data(message_lambda)
```

# Last but not least deploy
```sh
(.venv) ~/cloud-app-cdk $ cdk deploy cloud-app-cdk
```

# Test your app
Write a message (remember to use to correct endpoint):
```sh
(.venv) ~/cloud-app-cdk $ curl -X POST "https://ns1y3l5xji.execute-api.eu-west-1.amazonaws.com/prod/message?author=johndoe&message=helloworld"
```
Read a message
```sh
(.venv) ~/cloud-app-cdk $ curl -X GET "https://ns1y3l5xji.execute-api.eu-west-1.amazonaws.com/prod/read?author=johndoe"
```

# Synth your first CDK application
```sh
~/cloud-app-cdk $ cdk synth
```

# Clean your room
```sh
(.venv) ~/cloud-app-cdk $ cdk destroy
(.venv) ~/cloud-app-cdk $ deactivate
~/cloud-app-cdk $ cd ..
~/ $ rm -rf cloud-app-cdk
```