from aws_cdk import core
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigw

class CloudAppCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Put lambda resource
        put_lambda = _lambda.Function(
            self, 'PutHandler',
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset('lambda'),
            handler='put.handler'
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=put_lambda,
        )
