import sys

import boto3
from time import sleep
import json

clientSqs = boto3.client('sqs')
clientDynamo = boto3.client('dynamodb')

# more info at http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Client.receive_message
# returns a dict
while (True):
	# poll the queue every 10 seconds and return a dict object with the result
	dictMessages = clientSqs.receive_message(
		# QueueUrl='https://sqs.us-east-1.amazonaws.com/477157386854/oktafun',

		# queue with dummy data
		QueueUrl='https://sqs.us-east-1.amazonaws.com/890665980307/aa-batch-credentials',

		# request all attributes
		AttributeNames=['All'],
		MessageAttributeNames=['All'],
		MaxNumberOfMessages=10,  # number of messages to get, max 10
		VisibilityTimeout=30,  # messages will be visible in the source queue after this time
		WaitTimeSeconds=10,
		ReceiveRequestAttemptId='string'
	)

	intNumberOfMessages=len(dictMessages['Messages'])
	print 'We received ' + str(intNumberOfMessages) + ' messages from the queue.'

	# print 'Here is the first message in the set: ' + dictMessage=dictMessages['Messages'][0]['Body']

	# print 'Here are all of the messages: \n' + str(dictMessages)

	# print 'This is the first message that we received: \n ' + str(dictMessage)

	# iterate through dictMessages and insert each message into a DynamoDB table
	# todo: POST each individual message to an API, for an example, see https://github.com/dixonaws/ServiceNowLambda/blob/master/CreateTicket.py
	for index in range(intNumberOfMessages):
		jsonMessage=dictMessages['Messages'][index]['Body']
		# jsonMessageAttributes=jsonMessagedictMessages['Messages'][index]['Body']['Attributes']

		# convert the json message body into a dictionary object
		dictMessage=json.loads(jsonMessage)
		# dictMessageAttributes=json.loads(dictMessage['Attributes'])

		# print 'dictMessage: ' + str(dictMessage)

		# print 'This should be attributes: ' + str(dictMessages['Messages'][index]['Attributes'])
		strMessageReceiptHandle=str(dictMessages['Messages'][index]['ReceiptHandle'])

		# now we can manipulate individual key/values
		sys.stdout.write('Adding ' + dictMessage['email'] + '... ')
		dictResponse = clientDynamo.put_item(
			TableName='aa-batch-credentials',
			Item={
				'id': {
					'S': str(dictMessage['id'])
				},
				'first_name': {
					'S': str(dictMessage['first_name'])
				},
				'last_name': {
					'S': str(dictMessage['last_name'])
				},
				'email': {
					'S': str(dictMessage['email'])
				},
				'algorithm': {
					'S': str(dictMessage['algorithm'])
				},
				'hash': {
					'S': str(dictMessage['hash'])
				},
				'abo': {
					'S': str(dictMessage['abo'])
				}

			}
		)

		# if we get a 200 message from Dynano, then we have inserted the message into the table
		if(dictResponse['ResponseMetadata']['HTTPStatusCode'] == 200):
			print '200, Ok (we can expire message with receiptHandle beginning with: ' + strMessageReceiptHandle[0:15] + '... )'
			# todo: expire the message in SQS


	sleep(10)

# while(True)
