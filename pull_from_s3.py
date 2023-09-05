from pathlib import Path 
import os
import boto3

s3 = boto3.client('s3')

folder = "project_goes_here/target"

files = [
    "manifest.json",
    "index.html", # doing this to check that the download is correct
]

bucket = os.environ.get('AWS_S3_BUCKET')

def get_docs_from_s3():
    target_dir = Path(os.getcwd()) / folder
    if not target_dir.exists():
        target_dir.mkdir()
    try:
        for f in files:
            s3.download_file(
                bucket,
                f,
                str(os.path.join(os.getcwd(), folder, f))
            )
    except Exception as e:
        print("The following file could not be downloaded: " + f)
        print("Unexpected Error: " + str(e))

if __name__ == "__main__":
    get_docs_from_s3()
