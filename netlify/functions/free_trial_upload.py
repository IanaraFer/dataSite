import os
import json
from http import HTTPStatus

def handler(event, context):
    # Netlify passes files in multipart/form-data via event['body'] (base64-encoded) and event['isBase64Encoded']
    # For simple demo, just echo back the fields and file name (no actual storage)
    try:
        # Only allow POST
        if event.get('httpMethod', '').upper() != 'POST':
            return {
                'statusCode': HTTPStatus.METHOD_NOT_ALLOWED,
                'body': json.dumps({'error': 'Method not allowed'}),
                'headers': {'Allow': 'POST'}
            }
        # Netlify passes multipart/form-data as base64-encoded body
        import base64
        from io import BytesIO
        from cgi import FieldStorage
        
        body = event['body']
        if event.get('isBase64Encoded'):
            body = base64.b64decode(body)
        else:
            body = body.encode('utf-8')
        environ = {
            'REQUEST_METHOD': 'POST',
            'CONTENT_TYPE': event['headers'].get('content-type') or event['headers'].get('Content-Type'),
            'CONTENT_LENGTH': str(len(body)),
        }
        fp = BytesIO(body)
        form = FieldStorage(fp=fp, environ=environ, keep_blank_values=True)
        # Extract fields
        fields = {k: form.getvalue(k) for k in form.keys() if k != 'businessData'}
        fileitem = form['businessData'] if 'businessData' in form else None
        fileinfo = None
        if fileitem is not None and fileitem.filename:
            fileinfo = {
                'filename': fileitem.filename,
                'size': len(fileitem.file.read()),
                'type': fileitem.type
            }
        return {
            'statusCode': 200,
            'body': json.dumps({'fields': fields, 'file': fileinfo}),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
