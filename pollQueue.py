import boto3
from time import sleep

clientSqs=boto3.client('sqs')

# more info at http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Client.receive_message
# returns a dict
while(True):
    dictMessages=clientSqs.receive_message(
        # QueueUrl='https://sqs.us-east-1.amazonaws.com/477157386854/oktafun',
        QueueUrl='https://sqs.us-east-1.amazonaws.com/890665980307/aa-batch-credentials',

        AttributeNames=['All'],
        MessageAttributeNames=['All'],
        MaxNumberOfMessages=10,
        VisibilityTimeout=30,
        WaitTimeSeconds=10,
        ReceiveRequestAttemptId='string'
    )
    fileMessage = open('./tmp/message', 'a')
    fileMessage.write(str(dictMessages))
    fileMessage.close()

    sleep(10)
# while(True)



