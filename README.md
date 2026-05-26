# aws-cost-optimization
AWS Lambda automation to identify and delete stale EBS snapshots for cloud cost optimization using Python and Boto3.

# AWS EBS Snapshot Cleanup Automation

This project automates AWS cloud cost optimization by identifying and deleting stale EBS snapshots that are no longer associated with active EC2 instances.

## Technologies Used

* AWS Lambda
* Amazon EC2
* Amazon EBS
* Python
* Boto3
* IAM
* CloudWatch

## Features

* Detects stale EBS snapshots
* Validates attached volumes
* Checks running EC2 instances
* Deletes unused snapshots automatically
* Handles missing/deleted volumes using exception handling

## Future Improvements

* Multi-region support
* Dry-run mode
* SNS email alerts
* Tag-based filtering
* CloudWatch metrics dashboard
