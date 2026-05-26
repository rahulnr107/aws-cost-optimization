import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Get all EBS snapshots
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Get all running EC2 instance IDs
    instances_response = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )

    active_instance_ids = set()

    for reservation in instances_response['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance['InstanceId'])

    # Iterate through each snapshot
    for snapshot in response['Snapshots']:

        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        if not volume_id:
            # Delete snapshot if no associated volume
            ec2.delete_snapshot(SnapshotId=snapshot_id)

            print(
                f"Deleted EBS snapshot {snapshot_id} "
                f"as it was not attached to any volume."
            )

        else:
            try:
                # Check if volume exists
                volume_response = ec2.describe_volumes(
                    VolumeIds=[volume_id]
                )

                attachments = volume_response['Volumes'][0]['Attachments']

                # Delete if volume is not attached
                if not attachments:

                    ec2.delete_snapshot(SnapshotId=snapshot_id)

                    print(
                        f"Deleted EBS snapshot {snapshot_id} "
                        f"as volume was not attached."
                    )

                else:
                    # Check if attached instance is running
                    attached_instance_id = attachments[0]['InstanceId']

                    if attached_instance_id not in active_instance_ids:

                        ec2.delete_snapshot(SnapshotId=snapshot_id)

                        print(
                            f"Deleted EBS snapshot {snapshot_id} "
                            f"as volume was not attached to a running instance."
                        )

            except ec2.exceptions.ClientError as e:

                if e.response['Error']['Code'] == 'InvalidVolume.NotFound':

                    # Delete snapshot if associated volume is deleted
                    ec2.delete_snapshot(SnapshotId=snapshot_id)

                    print(
                        f"Deleted EBS snapshot {snapshot_id} "
                        f"as associated volume was not found."
                    )