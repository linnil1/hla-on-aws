import json
import boto3
import botocore
import settings


def setStatus(name, status="None", method=None):
    s3 = boto3.client('s3')
    try:
        data = json.load(s3.get_object(Bucket=settings.s3_bucket_name,
                                       Key=name + ".json")['Body'])
    except botocore.exceptions.ClientError:
        data = {}

    if not method:
        data['status'] = status
    else:
        data['result'] = data.get('result', {})
        data['result'][method] = data['result'].get(method, {})
        data['result'][method]['status'] = status

    s3.put_object(Bucket=settings.s3_bucket_name,
                  Key=name + ".json",
                  Body=json.dumps(data))
    return data


def setMethodResult(name, method, result):
    s3 = boto3.client('s3')
    # not need to double check
    data = json.load(s3.get_object(Bucket=settings.s3_bucket_name,
                                   Key=name + ".json")['Body'])
    data['result'] = data.get('result', {})
    data['result'][method] = result
    s3.put_object(Bucket=settings.s3_bucket_name,
                  Key=name + ".json",
                  Body=json.dumps(data))


def upload(path_file, new_filename):
    s3 = boto3.client('s3')
    response = s3.upload_file(path_file, settings.s3_bucket_name, new_filename)
