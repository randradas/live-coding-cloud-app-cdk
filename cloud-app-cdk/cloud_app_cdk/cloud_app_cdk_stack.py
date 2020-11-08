from aws_cdk import core
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_dynamodb as dynamodb

class CloudAppCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

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

        # Hello lambda
        hello_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='hello.handler'
        )

        # API Gateway
        cloud_app_apigw = apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_lambda,
        )

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
