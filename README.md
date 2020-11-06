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

## Init app structure
```
README.md
app.py           <--- entry point
cdk.json         <--- instructionns for cdk toolkit
cloud_app_cdk    <--- cloud application code
requirements.txt
setup.py
source.bat
```
