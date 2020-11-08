# What is this repo?

This repo is the code base used for the talk '*Live Coding Cloud Apps with CDK (infrastructure as code)*'.

Following this README.md will guide you to create your first cloud application
using AWS CDK. CDK is a set of assets that will help you to write infrastructure
as code using your favorite language (Typescript, Python, Javascrip, Go and
others), for more information about CDK take a look at
[this](https://docs.aws.amazon.com/cdk/latest/guide/home.html).

The result of this live coding session can be find at the '*/cloud-app-cdk/*'
directory. **This is not production ready code** and probably not the best
styled code but it works when it comes to understand how to develop with CDK.

# Thank you to...
It is inspired by
[cdkworkshop.com](https://cdkworkshop.com/),
[@darkosubotica](https://twitter.com/darkosubotica) talks,
[cdkday.com](https://www.cdkday.com/),
[awsome-cdk](https://github.com/kolomied/awesome-cdk) repository and
[cdk.dev](https://cdk.dev).
I would like to thank all of them which provided a lot of resources that
allowed me to learn the basis about CDK and bring it to my collegues.

# Let's get started!
This document is intended to guide you in the process of building your first
cloud application with CDK so it is divided in a few sections where you will do
something neecessary for the next section, this is better do no try to hurry up
and avoid a section since you could regret it in the following ones.

Note: it is important to know that you need a AWS account with environment
variables set with AWS credentials.

## Install CDK
### MacOS
Pre-requisites: [brew](https://brew.sh/)
```sh
~ $ brew install node
~ $ npm i -g aws-cdk
```

## Init app && prepare virtualenv
```sh
~ $ mkdir cloud-app-cdk
~ $ cd cloud-app-cdk
~/cloud-app-cdk $ cdk init --language python       <--- it will init a CDK boilerplate code
~/cloud-app-cdk $ source .venv/bin/activate
~/cloud-app-cdk $ pip install -r requirements.txt
```
## CDK app structure
```
README.md
app.py            <--- entry point
cdk.json          <--- instructionns for cdk toolkit
cloud_app_cdk     <--- cloud application code
requirements.txt
setup.py
source.bat
```
# (Phase 0): Bootstraping your AWS account
You need some AWS resources that will be used by the CDK toolkit to deploy your
app.
```
~/cloud-app-cdk $ cdk bootstrap
```
This will create a new AWS CloudFormation stack in your AWS account. It is only
necessary to be run one time.

# (Phase 1) Let's deploy something
At this point you will learn how to deploy something into your AWS account,
let's start with a lambda function that will be useful in further phases.

In order to be able to do it you need to install the AWS Lambda construct
library which will allow you to use the lambda construct in your CDK code.
## Lambda construct library
In order to use lambda you need to install the lambda construct library which
will provide AWS Lambda resources.
```sh
$ pip install aws-cdk.aws-lambda
```

Just put your lambda code as follow in the CDK app root directory.
```sh
~/cloud-app-cdk $ mkdir lambda
~/cloud-app-cdk $ vim lambda/hello.py
```

For learning purposes it is enough with a 'Hello World!' lambda like this:
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

## New lambda resource
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

        # Hello lambda resource
        hello_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='hello.handler'
        )
```
## Deploy
Now it's time to deploy your CDK application for the first time.
```sh
~/cloud-app-cdk $ cdk deploy cloud-app-cdk
```
You can check you AWS account at CloudFormation service and you will notice
a new CloudFormation stack is created.

# (Phase 2) API Gateway
A typical resource necessary in cloud application is an API, this resource
usually requires a lot of lines of code when you are coding AWS CloudFormation,
however let's see how it looks in CDK.
## Install API Gateway construct library
Again, you need to install the python package that contains the AWS APIGateway
construct library. It is always you need to do when using a construct library.
```sh
~/cloud-app-cdk $ pip install aws-cdk.aws_apigateway
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
        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_lambda,
        )
```
## Diff
Before trying to deploy again the changes let's see what is different between
the local cdk application and the one deployed.
```sh
~/cloud-app-cdk $ cdk diff cloud-app-cdk
```
## Deploy
It looks good and obviously new resources are going to be deployed as shown in
the '*cdk diff*' before.
```sh
~/cloud-app-cdk $ cdk deploy cloud-app-cdk
```
![New API gateway resources](./assets/apigw_resources.png)
As you see it will add twelve new resources.

## Test
```
Outputs:
cloud-app-cdk.Endpoint8024A810 = https://jmedoa58w2.execute-api.eu-west-1.amazonaws.com/pro

~/cloud-app-cdk $ curl https://jmedoa58w2.execute-api.eu-west-1.amazonaws.com/prod/
Hello, CDK! You have hit /
```

# (Phase 3) DynamoDB & Writing lambda
```sh
~/cloud-app-cdk $ pip install aws-cdk.dynamodb
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
                name='message',
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
            handler='message.handler'
        )
        cloud_app_apigw_integration = apigw.LambdaIntegration(message_lambda)
        api_message = cloud_app_apigw.root.add_resource("message")
        api_message.add_method("POST", cloud_app_apigw_integration)
```

# (Phase 4) Reading lambda
# (Phase 6) Permissions
# (Phase 7) Test your app
## Synth your first CDK application
```sh
cdk synth
```