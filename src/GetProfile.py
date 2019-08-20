import boto3
import json

dynamodb = boto3.resource('dynamodb')

def profileType(i):
    switcher={
            0:'Name',
            1:'Summary',
            2:'Header',
            3:'Highlight',
            4:'Skill'
            }
    return switcher.get(i, i)

def lambda_handler(event, context):
    table = dynamodb.Table('Profile')
    response = table.scan()
    items = response['Items']

    for idx, a in enumerate(items):
        current = items[idx]
        current['Type'] = profileType(current['Type'])
        items[idx] = {k.lower(): v for k, v in current.items()}

    profile = {}
    profile['items'] = sorted(items, key=lambda x : x['id'])   

    return profile