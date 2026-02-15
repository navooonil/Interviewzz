import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import HTTPException
import os
from ..config import settings
from ..utils.helpers import log_debug_message

class S3Service:
    """
    Handles uploading files to AWS S3.
    """
    def __init__(self):
        self.s3_client = None
        if settings.use_s3_storage:
            try:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.aws_access_key_id,
                    aws_secret_access_key=settings.aws_secret_access_key,
                    region_name=settings.aws_region
                )
                log_debug_message("Initialized S3 Client")
            except Exception as e:
                log_debug_message(f"Failed to initialize S3 client: {e}")

    def upload_file(self, file_path: str, object_name: str = None) -> str:
        """
        Uploads a file to an S3 bucket.
        
        Args:
            file_path: File to upload
            object_name: S3 object name. If not specified then file_name is used
            
        Returns:
            The public URL or S3 URI if successful
        """
        if not self.s3_client:
            log_debug_message("S3 upload skipped (not configured)")
            return file_path # Keep local path if S3 is off

        if object_name is None:
            object_name = os.path.basename(file_path)

        try:
            self.s3_client.upload_file(file_path, settings.s3_bucket_name, object_name)
            
            # Construct a simpler URL if bucket is public, or pre-signed URL if private.
            # For simplicity, we return the s3:// URI for now as a reference.
            s3_uri = f"s3://{settings.s3_bucket_name}/{object_name}"
            log_debug_message(f"Uploaded to S3: {s3_uri}")
            return s3_uri
            
        except FileNotFoundError:
            log_debug_message("The file was not found")
            return None
        except NoCredentialsError:
            log_debug_message("Credentials not available")
            return None
        except Exception as e:
            log_debug_message(f"S3 Upload Error: {e}")
            return None

# Singleton instance
s3_service = S3Service()
