import json
import boto3

print('Loading function')

# S3 boto3 client
s3 = boto3.client('s3')

# SNS boto3 client
sns = boto3.client("sns")

# create an SNS topic. then add destination -> SNS 
# SNS topic ARN
sns_topic_arn = "arn:aws:sns:us-west-2:285288445368:email"

def lambda_handler(event, context):  
    # Super useful documentation for this task 
    # AWS Boto3 - the AWS SDK
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
    
    # Bucket name
    bucket = "mybucket126584"
    
    # call list_objects on s3 to get latest object, returns only 1 object key when MaxKeys=1 
    response = s3.list_objects_v2(Bucket=bucket) 
    
    # Extract key name(name of .txt) from JSON response above
    key = response["Contents"][-1]["Key"]  
    
    try:
        # call get_object on s3 to retrieve file, using key and bucket from code above
        response = s3.get_object(Bucket=bucket, Key=key) 
        
        # the code needed to make an array containing all individual words from the file
        txtContent = response["Body"].read().decode("utf-8").split(" ")
        
        # publish results via boto3 SNS client
        sns.publish(
        TopicArn=sns_topic_arn,
        Message= f"\nA new file hast been uploaded to {bucket}.\nThe file {key} contains {len(txtContent)} individual words.",
        Subject='S3 Lambda word count'
        )
        
        
        # returning key(filename) and the length of the word array
        return f"{key} contains {len(txtContent)} words."
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e