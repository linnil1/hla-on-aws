import os
import json
import boto3
import utils
import settings


def main(event, context):
    name = event['name']

    base = f"{settings.data_folder}/{name}"
    os.makedirs(base, exist_ok=True)

    read1 = f"{base}/{name}.R1.fq.gz"
    read2 = f"{base}/{name}.R2.fq.gz"

    # download
    utils.setStatus(name, "Running")
    s3 = boto3.client('s3')
    s3.download_file(settings.s3_bucket_name, os.path.basename(read1), read1)
    s3.download_file(settings.s3_bucket_name, os.path.basename(read2), read2)

    return {
        'name': name,
        'base': base,
        'read1': read1,
        'read2': read2,
    }
