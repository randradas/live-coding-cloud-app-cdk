# What is this repo?

This repo is the code base used for the talk '*Live Coding Cloud Apps with CDK (infrastructure as code)*'.

Also, includes documentation that guide you through the process of the live coding session setp by step to reach the finnal result.

The result of this live coding session can be find at the '*/cloud-app-cdk/*' directory.

# Let's get started!

## Init app && prepare virtualenv
```sh
mkdir cloud-app-cdk
cd cloud-app-cdk
cdk init --language python
source .venv/bin/activate
pip install -r requirements.txt
````

## CDK app structure
```
README.md
app.py           <--- entry point
cdk.json         <--- instructionns for cdk toolkit
cloud_app_cdk    <--- cloud application code
requirements.txt
setup.py
source.bat
```

## Bootstraping you AWS account
You need some resources that will be used by the CDK toolkitto deploy your app.

```
$ cdk bootstrap
```

# Some actual code (APIGW + Lambda)
## Lambda
### Lambda construct library
```sh
$ pip install aws-cdk.aws-lambda
```
```sh
$ mkdir lambda
$ vim lambda/put.py
```
### Lambda code
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
### Add lambda resource
```python
from aws_cdk import aws_lambda as _lambda
```
```python
# Put lambda resource
put_lambda = _lambda.Function(
    self, 'PutHandler',
    runtime=_lambda.Runtime.PYTHON_3_8,
    code=_lambda.Code.asset('lambda'),
    handler='put.handler'
)
```

### Deploy
```sh
$ cdk deploy cloud-app-cdk
```

## API Gateway
### Install construct
```sh
$ pip install aws-cdk.aws_apigateway
```
### Add API Gateway resource
```python
apigw.LambdaRestApi(
    self, 'Endpoint',
    handler=my_lambda,
)
```
### Diff
```sh
$ cdk diff cloud-app-cdk
```
### Deploy
```sh
$ cdk deploy cloud-app-cdk
```

## Test
```
Outputs:
cloud-app-cdk.Endpoint8024A810 = https://jmedoa58w2.execute-api.eu-west-1.amazonaws.com/pro

$ curl https://jmedoa58w2.execute-api.eu-west-1.amazonaws.com/prod/
Hello, CDK! You have hit /
```

## Synth your first CDK application
```sh
cdk synth
```