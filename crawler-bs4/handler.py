import requests
from bs4 import BeautifulSoup
import datetime
import json
import validators

def main(event, context):
    validationResponse = validateRequest(event)

    if 'error' in validationResponse:
        return sendError(validationResponse['error']['message'], validationResponse['error']['statusCode'])
    
    url = event['queryStringParameters']['url']

    data = {
        'url': url,
        'date': str(datetime.datetime.now()),
        'product': parse(url)
    }

    return sendSuccess(data)

def parse(url):
    titleSelector = '.product-title'
    descriptionSelector = '.box-lower-content .p2'
    priceSelector = '.p1.price'

    page = requests.get(url)
    content = BeautifulSoup(page.content, 'html.parser')

    if content.select(titleSelector):
        title = content.select(titleSelector)[0].get_text()
    else:
        title = ''

    if content.select(descriptionSelector):
        description = content.select(descriptionSelector)[0].get_text()
    else:
        description = ''

    if content.select(priceSelector):
        price = content.select(priceSelector)[0].get_text()
    else:
        price = ''
    
    return {
        'product': {
            'title': title,
            'description': description,
            'price': price
        }
    }

def validateRequest(event):
    if event['queryStringParameters'] is None or not 'url' in event['queryStringParameters']:
        return {
            'error': {
                'statusCode': 400,
                'message': 'No url is provided.'
            }
        }             

    if not validators.url(event['queryStringParameters']['url']):
        return {
            'error': {
                'statusCode': 400,
                'message': 'Invalid url.'
            }
        } 
    
    return {}

def sendSuccess(data, statusCode = 200):
    body = {
        'success': True,
        'data': data
    }
    return sendJsonResponse(body, statusCode)

def sendError(message, statusCode = 500):
    body = {
        'success': False,
        'error': message
    }
    return sendJsonResponse(body, statusCode)

def sendJsonResponse(body, statusCode):
    return {
        'headers': {
            'Content-Type': 'application/json'
        },
        'statusCode': statusCode,
        'body': json.dumps(body)
    }

if __name__ == '__main__':
    main('', '')