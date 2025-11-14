# ☁️ Cloud Platforms Integration with Python

## Complete Professional Guide to AWS, Azure, and GCP

---

## Table of Contents

1. [AWS (Amazon Web Services)](#1-aws-amazon-web-services)
2. [Microsoft Azure](#2-microsoft-azure)
3. [Google Cloud Platform (GCP)](#3-google-cloud-platform)
4. [Multi-Cloud Patterns](#4-multi-cloud-patterns)
5. [Serverless Deployment](#5-serverless-deployment)

---

## 1. AWS (Amazon Web Services)

### 1.1 S3 (Simple Storage Service)

```python
import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
import os
from typing import List, Optional

class S3Manager:
    """Professional AWS S3 management"""

    def __init__(self, region_name='us-east-1'):
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.s3_resource = boto3.resource('s3', region_name=region_name)

        # Configure multipart upload
        self.transfer_config = TransferConfig(
            multipart_threshold=1024 * 25,  # 25 MB
            max_concurrency=10,
            multipart_chunksize=1024 * 25,
            use_threads=True
        )

    def create_bucket(self, bucket_name: str, region: str = None):
        """Create S3 bucket"""
        try:
            if region is None:
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': region}
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration=location
                )
            print(f"✓ Bucket created: {bucket_name}")
        except ClientError as e:
            print(f"✗ Error creating bucket: {e}")

    def upload_file(self, file_path: str, bucket: str, object_name: str = None):
        """Upload file to S3"""
        if object_name is None:
            object_name = os.path.basename(file_path)

        try:
            self.s3_client.upload_file(
                file_path,
                bucket,
                object_name,
                Config=self.transfer_config
            )
            print(f"✓ Uploaded: {file_path} → s3://{bucket}/{object_name}")
            return True
        except ClientError as e:
            print(f"✗ Upload failed: {e}")
            return False

    def download_file(self, bucket: str, object_name: str, file_path: str):
        """Download file from S3"""
        try:
            self.s3_client.download_file(bucket, object_name, file_path)
            print(f"✓ Downloaded: s3://{bucket}/{object_name} → {file_path}")
            return True
        except ClientError as e:
            print(f"✗ Download failed: {e}")
            return False

    def list_files(self, bucket: str, prefix: str = '') -> List[str]:
        """List files in bucket"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix
            )

            if 'Contents' in response:
                return [obj['Key'] for obj in response['Contents']]
            return []
        except ClientError as e:
            print(f"✗ Error listing files: {e}")
            return []

    def delete_file(self, bucket: str, object_name: str):
        """Delete file from S3"""
        try:
            self.s3_client.delete_object(Bucket=bucket, Key=object_name)
            print(f"✓ Deleted: s3://{bucket}/{object_name}")
            return True
        except ClientError as e:
            print(f"✗ Delete failed: {e}")
            return False

    def generate_presigned_url(self, bucket: str, object_name: str, expiration: int = 3600):
        """Generate presigned URL for temporary access"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': object_name},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            print(f"✗ Error generating URL: {e}")
            return None


# Usage
s3 = S3Manager()

# Create bucket
s3.create_bucket('my-app-bucket')

# Upload file
s3.upload_file('data.csv', 'my-app-bucket', 'uploads/data.csv')

# Download file
s3.download_file('my-app-bucket', 'uploads/data.csv', 'downloaded_data.csv')

# List files
files = s3.list_files('my-app-bucket', prefix='uploads/')
print(f"Files: {files}")

# Generate presigned URL (valid for 1 hour)
url = s3.generate_presigned_url('my-app-bucket', 'uploads/data.csv')
print(f"Temporary URL: {url}")
```

### 1.2 DynamoDB (NoSQL Database)

```python
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import json

class DynamoDBManager:
    """Professional DynamoDB management"""

    def __init__(self, region_name='us-east-1'):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.client = boto3.client('dynamodb', region_name=region_name)

    def create_table(self, table_name: str):
        """Create DynamoDB table"""
        try:
            table = self.dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'},  # Partition key
                    {'AttributeName': 'created_at', 'KeyType': 'RANGE'}  # Sort key
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                    {'AttributeName': 'created_at', 'AttributeType': 'S'},
                    {'AttributeName': 'user_id', 'AttributeType': 'S'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'UserIndex',
                        'KeySchema': [
                            {'AttributeName': 'user_id', 'KeyType': 'HASH'}
                        ],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

            table.wait_until_exists()
            print(f"✓ Table created: {table_name}")
            return table
        except ClientError as e:
            print(f"✗ Error creating table: {e}")
            return None

    def put_item(self, table_name: str, item: dict):
        """Insert item"""
        table = self.dynamodb.Table(table_name)

        try:
            table.put_item(Item=item)
            print(f"✓ Item inserted")
            return True
        except ClientError as e:
            print(f"✗ Error inserting item: {e}")
            return False

    def get_item(self, table_name: str, key: dict):
        """Get item by key"""
        table = self.dynamodb.Table(table_name)

        try:
            response = table.get_item(Key=key)
            return response.get('Item')
        except ClientError as e:
            print(f"✗ Error getting item: {e}")
            return None

    def query_by_partition_key(self, table_name: str, partition_key: str, value: str):
        """Query by partition key"""
        table = self.dynamodb.Table(table_name)

        try:
            response = table.query(
                KeyConditionExpression=Key(partition_key).eq(value)
            )
            return response['Items']
        except ClientError as e:
            print(f"✗ Error querying: {e}")
            return []

    def scan_with_filter(self, table_name: str, filter_expression):
        """Scan table with filter"""
        table = self.dynamodb.Table(table_name)

        try:
            response = table.scan(FilterExpression=filter_expression)
            return response['Items']
        except ClientError as e:
            print(f"✗ Error scanning: {e}")
            return []

    def update_item(self, table_name: str, key: dict, update_expression: str, expression_values: dict):
        """Update item"""
        table = self.dynamodb.Table(table_name)

        try:
            response = table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ReturnValues="UPDATED_NEW"
            )
            return response['Attributes']
        except ClientError as e:
            print(f"✗ Error updating item: {e}")
            return None

    def delete_item(self, table_name: str, key: dict):
        """Delete item"""
        table = self.dynamodb.Table(table_name)

        try:
            table.delete_item(Key=key)
            print(f"✓ Item deleted")
            return True
        except ClientError as e:
            print(f"✗ Error deleting item: {e}")
            return False


# Usage
db = DynamoDBManager()

# Create table
db.create_table('users')

# Insert item
db.put_item('users', {
    'id': '123',
    'created_at': '2024-01-01T00:00:00',
    'user_id': 'user123',
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30
})

# Get item
item = db.get_item('users', {'id': '123', 'created_at': '2024-01-01T00:00:00'})
print(item)

# Query by partition key
users = db.query_by_partition_key('users', 'id', '123')

# Scan with filter
active_users = db.scan_with_filter('users', Attr('age').gt(25))

# Update item
db.update_item(
    'users',
    {'id': '123', 'created_at': '2024-01-01T00:00:00'},
    'SET age = :val',
    {':val': 31}
)
```

### 1.3 Lambda Functions

```python
import boto3
import json
import zipfile
import io

class LambdaManager:
    """AWS Lambda management"""

    def __init__(self, region_name='us-east-1'):
        self.lambda_client = boto3.client('lambda', region_name=region_name)
        self.iam_client = boto3.client('iam', region_name=region_name)

    def create_lambda_role(self, role_name: str):
        """Create IAM role for Lambda"""
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        try:
            response = self.iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy)
            )

            # Attach basic execution policy
            self.iam_client.attach_role_policy(
                RoleName=role_name,
                PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
            )

            return response['Role']['Arn']
        except ClientError as e:
            print(f"✗ Error creating role: {e}")
            return None

    def create_deployment_package(self, function_code: str) -> bytes:
        """Create Lambda deployment package"""
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr('lambda_function.py', function_code)

        return zip_buffer.getvalue()

    def create_function(self, function_name: str, role_arn: str, handler: str, runtime: str, code: bytes):
        """Create Lambda function"""
        try:
            response = self.lambda_client.create_function(
                FunctionName=function_name,
                Runtime=runtime,
                Role=role_arn,
                Handler=handler,
                Code={'ZipFile': code},
                Timeout=30,
                MemorySize=128,
                Environment={
                    'Variables': {
                        'ENV': 'production'
                    }
                }
            )
            print(f"✓ Lambda function created: {function_name}")
            return response
        except ClientError as e:
            print(f"✗ Error creating function: {e}")
            return None

    def invoke_function(self, function_name: str, payload: dict):
        """Invoke Lambda function"""
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )

            result = json.loads(response['Payload'].read())
            return result
        except ClientError as e:
            print(f"✗ Error invoking function: {e}")
            return None


# Lambda function code
lambda_code = '''
import json

def lambda_handler(event, context):
    """Lambda function handler"""

    # Process event
    name = event.get('name', 'World')

    # Return response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Hello, {name}!'
        })
    }
'''

# Usage
lambda_mgr = LambdaManager()

# Create IAM role
role_arn = lambda_mgr.create_lambda_role('lambda-execution-role')

# Create deployment package
code = lambda_mgr.create_deployment_package(lambda_code)

# Create function
lambda_mgr.create_function(
    function_name='hello-world',
    role_arn=role_arn,
    handler='lambda_function.lambda_handler',
    runtime='python3.11',
    code=code
)

# Invoke function
result = lambda_mgr.invoke_function('hello-world', {'name': 'Python Developer'})
print(result)
```

---

## 2. Microsoft Azure

### 2.1 Azure Blob Storage

```python
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
import os

class AzureBlobManager:
    """Azure Blob Storage management"""

    def __init__(self, connection_string: str):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    def create_container(self, container_name: str):
        """Create container"""
        try:
            container_client = self.blob_service_client.create_container(container_name)
            print(f"✓ Container created: {container_name}")
            return container_client
        except ResourceExistsError:
            print(f"Container already exists: {container_name}")
            return self.blob_service_client.get_container_client(container_name)

    def upload_file(self, container_name: str, file_path: str, blob_name: str = None):
        """Upload file to blob storage"""
        if blob_name is None:
            blob_name = os.path.basename(file_path)

        blob_client = self.blob_service_client.get_blob_client(
            container=container_name,
            blob=blob_name
        )

        with open(file_path, 'rb') as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"✓ Uploaded: {file_path} → {container_name}/{blob_name}")

    def download_file(self, container_name: str, blob_name: str, download_path: str):
        """Download file from blob storage"""
        blob_client = self.blob_service_client.get_blob_client(
            container=container_name,
            blob=blob_name
        )

        with open(download_path, 'wb') as download_file:
            download_file.write(blob_client.download_blob().readall())

        print(f"✓ Downloaded: {container_name}/{blob_name} → {download_path}")

    def list_blobs(self, container_name: str):
        """List blobs in container"""
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_list = container_client.list_blobs()

        return [blob.name for blob in blob_list]

    def delete_blob(self, container_name: str, blob_name: str):
        """Delete blob"""
        blob_client = self.blob_service_client.get_blob_client(
            container=container_name,
            blob=blob_name
        )

        blob_client.delete_blob()
        print(f"✓ Deleted: {container_name}/{blob_name}")


# Usage
connection_string = "DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net"
azure_blob = AzureBlobManager(connection_string)

# Create container
azure_blob.create_container('mycontainer')

# Upload file
azure_blob.upload_file('mycontainer', 'data.csv')

# List blobs
blobs = azure_blob.list_blobs('mycontainer')
print(f"Blobs: {blobs}")

# Download file
azure_blob.download_file('mycontainer', 'data.csv', 'downloaded.csv')
```

### 2.2 Azure Functions

```python
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function HTTP trigger"""

    # Get query parameters
    name = req.params.get('name')

    # Get request body
    if not name:
        try:
            req_body = req.get_json()
            name = req_body.get('name')
        except ValueError:
            pass

    # Return response
    if name:
        return func.HttpResponse(
            f"Hello, {name}! This HTTP triggered function executed successfully.",
            status_code=200
        )
    else:
        return func.HttpResponse(
            "Please pass a name in the query string or request body.",
            status_code=400
        )


# Deploy with Azure Functions Core Tools
# func init MyFunctionProj --python
# func new --name HttpTrigger --template "HTTP trigger"
# func start
```

---

## 3. Google Cloud Platform (GCP)

### 3.1 Google Cloud Storage

```python
from google.cloud import storage
from google.cloud.exceptions import NotFound
import os

class GCSManager:
    """Google Cloud Storage management"""

    def __init__(self, project_id: str):
        self.client = storage.Client(project=project_id)

    def create_bucket(self, bucket_name: str, location='US'):
        """Create GCS bucket"""
        try:
            bucket = self.client.create_bucket(bucket_name, location=location)
            print(f"✓ Bucket created: {bucket_name}")
            return bucket
        except Exception as e:
            print(f"✗ Error creating bucket: {e}")
            return None

    def upload_file(self, bucket_name: str, file_path: str, destination_blob_name: str = None):
        """Upload file to GCS"""
        if destination_blob_name is None:
            destination_blob_name = os.path.basename(file_path)

        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(file_path)
        print(f"✓ Uploaded: {file_path} → gs://{bucket_name}/{destination_blob_name}")

    def download_file(self, bucket_name: str, source_blob_name: str, destination_file_name: str):
        """Download file from GCS"""
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)

        blob.download_to_filename(destination_file_name)
        print(f"✓ Downloaded: gs://{bucket_name}/{source_blob_name} → {destination_file_name}")

    def list_blobs(self, bucket_name: str, prefix: str = None):
        """List blobs in bucket"""
        blobs = self.client.list_blobs(bucket_name, prefix=prefix)
        return [blob.name for blob in blobs]

    def delete_blob(self, bucket_name: str, blob_name: str):
        """Delete blob"""
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.delete()
        print(f"✓ Deleted: gs://{bucket_name}/{blob_name}")


# Usage (requires GOOGLE_APPLICATION_CREDENTIALS environment variable)
gcs = GCSManager('my-project-id')

# Create bucket
gcs.create_bucket('my-gcs-bucket')

# Upload file
gcs.upload_file('my-gcs-bucket', 'data.csv')

# List blobs
blobs = gcs.list_blobs('my-gcs-bucket')
print(f"Blobs: {blobs}")

# Download file
gcs.download_file('my-gcs-bucket', 'data.csv', 'downloaded.csv')
```

---

## 4. Multi-Cloud Abstraction

### 4.1 Unified Cloud Storage Interface

```python
from abc import ABC, abstractmethod
from typing import List

class CloudStorage(ABC):
    """Abstract cloud storage interface"""

    @abstractmethod
    def upload_file(self, file_path: str, remote_path: str): pass

    @abstractmethod
    def download_file(self, remote_path: str, local_path: str): pass

    @abstractmethod
    def list_files(self, prefix: str = '') -> List[str]: pass

    @abstractmethod
    def delete_file(self, remote_path: str): pass


class AWSStorage(CloudStorage):
    """AWS S3 implementation"""

    def __init__(self, bucket: str):
        self.s3 = S3Manager()
        self.bucket = bucket

    def upload_file(self, file_path: str, remote_path: str):
        return self.s3.upload_file(file_path, self.bucket, remote_path)

    def download_file(self, remote_path: str, local_path: str):
        return self.s3.download_file(self.bucket, remote_path, local_path)

    def list_files(self, prefix: str = '') -> List[str]:
        return self.s3.list_files(self.bucket, prefix)

    def delete_file(self, remote_path: str):
        return self.s3.delete_file(self.bucket, remote_path)


class AzureStorage(CloudStorage):
    """Azure Blob implementation"""

    def __init__(self, container: str, connection_string: str):
        self.azure = AzureBlobManager(connection_string)
        self.container = container

    def upload_file(self, file_path: str, remote_path: str):
        return self.azure.upload_file(self.container, file_path, remote_path)

    def download_file(self, remote_path: str, local_path: str):
        return self.azure.download_file(self.container, remote_path, local_path)

    def list_files(self, prefix: str = '') -> List[str]:
        return self.azure.list_blobs(self.container)

    def delete_file(self, remote_path: str):
        return self.azure.delete_blob(self.container, remote_path)


class GCPStorage(CloudStorage):
    """GCP Cloud Storage implementation"""

    def __init__(self, bucket: str, project_id: str):
        self.gcs = GCSManager(project_id)
        self.bucket = bucket

    def upload_file(self, file_path: str, remote_path: str):
        return self.gcs.upload_file(self.bucket, file_path, remote_path)

    def download_file(self, remote_path: str, local_path: str):
        return self.gcs.download_file(self.bucket, remote_path, local_path)

    def list_files(self, prefix: str = '') -> List[str]:
        return self.gcs.list_blobs(self.bucket, prefix)

    def delete_file(self, remote_path: str):
        return self.gcs.delete_blob(self.bucket, remote_path)


# Usage - Switch cloud providers easily
def process_data(storage: CloudStorage):
    """Process data regardless of cloud provider"""
    storage.upload_file('data.csv', 'uploads/data.csv')
    files = storage.list_files('uploads/')
    print(f"Files: {files}")


# Use AWS
aws_storage = AWSStorage('my-s3-bucket')
process_data(aws_storage)

# Use Azure
azure_storage = AzureStorage('my-container', connection_string)
process_data(azure_storage)

# Use GCP
gcp_storage = GCPStorage('my-gcs-bucket', 'my-project')
process_data(gcp_storage)
```

---

This comprehensive cloud guide enables you to work with all major cloud providers using Python. Master these skills to build scalable cloud-native applications!
