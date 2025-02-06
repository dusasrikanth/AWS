import json
import boto3 
import time
def lambda_handler(event, context):
    client = boto3.client("ec2", region_name="ap-south-1")
    resp = client.describe_volumes().get("Volumes", [])
    unattachedvols = []
    time.sleep(15)
    for vol in resp:
        if len(vol["Attachments"]) == 0:
            volid = vol["VolumeId"]
            print(f"Volume {volid} is not attached and will be deleted")
            unattachedvols.append(vol["VolumeId"])
        else:
            volid = vol["VolumeId"]
            """print(f"Volume {volid} is attached")"""

    print(f"The Volumes which are availible are {unattachedvols}")
    ec2_resource = boto3.resource("ec2", region_name="ap-south-1")
    for vol in unattachedvols:
        print(vol)
        volume = ec2_resource.Volume()
        volume.delete()