import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb')

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(CustomEncoder, self).default(o)

def lambda_handler(event, context):
    table = dynamodb.Table('Jobs')
    response = table.scan()
    jsonString = json.dumps(response['Items'], cls=CustomEncoder)
    itemsObject = json.loads(jsonString)

    result = {}
    items = []

    for item in itemsObject:
        lowerCaseDict = {k.lower(): v for k, v in item.items()}
        items.append(lowerCaseDict)

    
    result['items'] = sorted(items, key=lambda x : x['id'])

    return result