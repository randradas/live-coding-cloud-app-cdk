#!/usr/bin/env python3

from aws_cdk import core

from cloud_app_cdk.cloud_app_cdk_stack import CloudAppCdkStack


app = core.App()
CloudAppCdkStack(app, "cloud-app-cdk")

app.synth()
