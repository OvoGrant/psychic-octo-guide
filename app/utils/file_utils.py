import boto3
import uuid
from botocore.config import Config
import os




AWS_S3_BUCKET_NAME = "psychic-octopus"

session = boto3.session.Session()
client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com',
                        aws_access_key_id=os.getenv("SPACES_KEY"),
                        aws_secret_access_key=os.getenv("SPACES_SECRET"))


def write_to_s3(file):
    s3_file_name = f"{uuid.uuid4()}.mp3" 
    try:
        with open ("local.mp3", "wb") as f:
            for chunk in file:
                if chunk:
                    f.write(chunk)

        with open ("local.mp3", "rb") as f:
            client.put_object(
            Bucket=AWS_S3_BUCKET_NAME,
            Key= "audios/" + s3_file_name,
            Body=f,
            ACL="private",
            Metadata={ # Defines metadata tags.
                      'x-amz-meta-my-key': 'your-value'
            }
        )
    except Exception as e:
        print(f"Error uploading file: {e}")
    return s3_file_name

def cleanup():
    file_path = "local.mp3"
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    else:
        print(f"{file_path} does not exist.")

def generate_presigned_url(s3_file_name: str) -> str:
    signed_url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": AWS_S3_BUCKET_NAME, "Key": "audios/" + s3_file_name},
        ExpiresIn=3600,
    )  # URL expires in 1 hour
    return signed_url



def write_to_local_disk(file):
    pass


