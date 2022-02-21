import re
import json
import uuid
import boto3
import botocore
import utils
import settings


def getObject(name):
    s3 = boto3.client('s3')
    try:
        return s3.get_object(Bucket=settings.s3_bucket_name, Key=name)
    except botocore.exceptions.ClientError:
        return None


def getJobMain(name):
    data = getObject(name + ".json")
    if data:
        return json.load(data['Body'])
    return {'status': "Not Found"}


def getPlainText(file):
    data = getObject(file)
    if data:
        return data['Body'].read().decode()
    return ""


def checkFile(file):
    s3 = boto3.client('s3')
    try:
        s3.get_object(Bucket=settings.s3_bucket_name, Key=file)
        return True
    except botocore.exceptions.ClientError:
        return False


def checkFastqStatus(name):
    return checkFile(name + ".R1.fq.gz") and checkFile(name + ".R2.fq.gz")
    # TODO check gz
    return True


def checkTriggered(name):
    data = getJobMain(name)
    return data['status'] != "Init" and data['status'] != "Not Found"


def startJob(name):
    region = settings.stateMachineArn.split(":")[3]
    step = boto3.client('stepfunctions', region_name=region)
    response = step.start_execution(
        stateMachineArn=settings.stateMachineArn,
        name=f'hla-{name}',
        input=json.dumps({'name': name})
    )
    return {'status': "OK", 'startDate': response['startDate'].isoformat()}


def create_presigned_post(bucket_name, object_name, expiration=3600):
    """
    Create a URL that allow anyone to upload their file.

    Reference:
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html

    Return:
        A URL str
    """
    s3 = boto3.client('s3')
    try:
        response = s3.generate_presigned_post(bucket_name,
                                              object_name,
                                              ExpiresIn=expiration)
    except botocore.exceptions.ClientError as e:
        return None
    return response


def findNewId():
    # return "test2"
    s3 = boto3.client('s3')
    while True:
        name = str(uuid.uuid4()).split('-')[0]
        try:
            s3.get_object(Bucket=settings.s3_bucket_name,
                          Key=name + ".json")
        except botocore.exceptions.ClientError:
            return name


def createTask():
    name = findNewId()
    utils.setStatus(name, "Init")
    read1 = create_presigned_post(settings.s3_bucket_name, f"{name}.R1.fq.gz")
    read2 = create_presigned_post(settings.s3_bucket_name, f"{name}.R2.fq.gz")

    # TODO implement
    return {
        'name': name,
        'read1': read1,
        'read2': read2,
    }


def returnError(statusCode, status):
    return {
        "statusCode": str(statusCode),
        'body': json.dumps({
            'status': status,
        })
    }


def main(event, context):
    if event['path'] == "/create" and event['httpMethod'] == "POST":
        return {'body': json.dumps(createTask())}

    if (re.match(r"^/task/\w+/status", event['path'])
            and event['httpMethod'] == "POST"):
        name = re.match(r"/task/(\w+)/status", event['path']).group(1)
        return {'body': json.dumps(getJobMain(name))}

    if (re.match(r"^/task/\w+/submit", event['path'])
            and event['httpMethod'] == "POST"):
        name = re.match(r"/task/(\w+)/submit", event['path']).group(1)
        if checkTriggered(name):
            return returnError(403, "Already run it")
        elif not checkFastqStatus(name):
            return returnError(403, "Not upload Yet")
        return {'body': json.dumps(startJob(name))}

    if (re.match(r"^/task/\w+/show/.+", event['path'])
            and event['httpMethod'] == "POST"):
        m = re.match(r"^/task/(\w+)/show/(.+)", event['path'])
        name, file = m.group(1), m.group(2)
        if not file.startswith(name):
            return returnError(403, "Filename Error")
        if not checkFile(file):
            return returnError(404, "Cannot find filename")
        return {'body': getPlainText(file)}

    return returnError(404, "not found")


# testing example
# print(main({'path': "/create", 'httpMethod': "POST"}, None))
# print(main({'path': "/task/test2/status", 'httpMethod': "POST"}, None))
