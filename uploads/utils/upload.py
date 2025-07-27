import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

session = boto3.session.Session()
client = session.client(
    service_name='s3',
    endpoint_url=settings.ARVAN_ENDPOINT,
    aws_access_key_id=settings.ARVAN_ACCESS_KEY,
    aws_secret_access_key=settings.ARVAN_SECRET_KEY,
)

BUCKET_NAME = settings.ARVAN_BUCKET

def upload_file_to_arvan(file_obj, key):
    try:
        client.upload_fileobj(file_obj, BUCKET_NAME, key)
        logger.debug(f"Uploaded file to Arvan: {key}")
        return True
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return False

def delete_file_from_arvan(key):
    try:
        if key:
            client.delete_object(Bucket=BUCKET_NAME, Key=key)
            logger.debug(f"Deleted file from Arvan: {key}")
    except Exception as e:
        logger.error(f"Delete error: {e}")

def generate_presigned_url(key, expiration=3600):
    try:
        url = client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': key},
            ExpiresIn=expiration,
        )
        return url
    except ClientError as e:
        logger.error(f"Presigned URL error: {e}")
        return None
