import boto3

clientSqs=boto3.client('sqs')

# more info at http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Client.receive_message
# returns a dict
dictMessages=clientSqs.receiveMessage(
    queryUrl='',
    AttributeNames='All',
    MessageAttributeNames='All',
    MaxNumberOfMessages=10,
    VisibilityTimeout=30,
    WaitTimeSeconds=10,
    ReceiveRequestAttemptId='string'
)

print(dictMessages)


