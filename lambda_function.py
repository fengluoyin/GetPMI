from botocore.vendored import requests
from lxml import html
import json
import boto3
import os

def lambda_handler(event, context):
	page = requests.get('https://www.markiteconomics.com/public')
	tree = html.fromstring(page.content)
	#This will create a list of buyers:
	pmi = tree.xpath('//span[@class="indexFigure"]/text()')
	#This will create a list of prices
	country = tree.xpath('//span[@class="indexName"]/text()')


	list = zip(country, pmi)
	str = ""
	for i in list:
	    str = str + ':   '.join(i) + "\n"
	message = [{'country': cou, 'pmi': p} for cou, p in zip(country, pmi)]

	SNS = os.environ['SNS']
	print SNS
	message = {"foo": "bar"}
	client = boto3.client('sns')
	response = client.publish(
    	TargetArn=SNS,
    	Message=str,
    	MessageStructure='string',
	)

	return "Succeed"