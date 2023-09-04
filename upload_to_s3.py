# from pathlib import Path 
import os
import boto3
import mimetypes 

s3 = boto3.client('s3')

folder = "project_goes_here/target"

files = [
    "manifest.json",
    "index.html",
    "catalog.json",
]

bucket = os.environ.get('AWS_S3_BUCKET')
print(bucket)

def push_docs_to_s3():
    for f in files:
        if mimetypes.guess_type(f)[0] is not None:
            s3.upload_file(
                str(os.path.join(os.getcwd(), folder, f)),
                bucket,
                f,
                ExtraArgs={"ContentType": mimetypes.guess_type(f)[0]},
            )
        elif mimetypes.guess_type(f)[0] is None:
            try:
                with open(str(os.path.join(os.getcwd(), folder, f)), "rb") as data:
                    s3.upload_fileobj(
                        data,
                        bucket,
                        f)
            except Exception as e:
                print("The following file could not be uploaded: " + f)
                print("Unexpected Error: " + e)
        else:
            raise Exception(
                "One of the files being uploaded is of an undefined file type: " + f
            )

if __name__ == "__main__":
    push_docs_to_s3()