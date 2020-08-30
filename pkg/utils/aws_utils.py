import os

import boto3


def sync_resources(bucket_name, resource_prefix, local_path):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    for obj in bucket.objects.filter(Prefix=resource_prefix):
        if obj.key[-1] != "/" and not os.path.exists(obj.key):  # Ignore S3 'folders'
            print(f'Downloading {obj.key}...')
            bucket.download_file(obj.key, obj.key)
