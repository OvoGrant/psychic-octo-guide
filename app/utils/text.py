
# Step 1: Import the all necessary libraries and SDK commands.
import os
import boto3
import botocore

# Step 2: The new session validates your request and directs it to your Space's specified endpoint using the AWS SDK.
session = boto3.session.Session()
client = session.client('s3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com', # Find your endpoint in the control panel, under Settings. Prepend "https://".
                        config=botocore.config.Config(s3={'addressing_style': 'virtual'}), # Configures to use subdomain/virtual calling format.
                        region_name='nyc3', # Use the region in your endpoint.
                        aws_access_key_id='JMTbKcLOMnxiEV/YWMWwPcZbvZxy2+cGbfRbSuswvf0', # Access key pair. You can create access key pairs using the control panel or API.
                        aws_secret_access_key='DO801HPLG6LXYRMN3ZME') # Secret access key defined through an environment variable.

# Step 3: Call the put_object command and specify the file to upload.
client.put_object(Bucket='example-space-name', # The path to the directory you want to upload the object to, starting with your Space name.
                  Key='folder-path/hello-world.txt', # Object key, referenced whenever you want to access this file later.
                  Body=b'psychic-octopus', # The object's contents.
                  ACL='private', # Defines Access-control List (ACL) permissions, such as private or public.
                  Metadata={ # Defines metadata tags.
                      'x-amz-meta-my-key': 'your-value'
                  }
                )