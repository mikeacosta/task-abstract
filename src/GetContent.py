import boto3
import json

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('Content')
    response = table.scan()
    json_tree = json.dumps(response['Items'])
    items = json.loads(json_tree)

    data = {}

    for item in items:
        data[item['Name']] = item['Value']
        
    return data   