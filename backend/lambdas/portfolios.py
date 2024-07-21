import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()

def created_event(event):
    # Your logic here
    return {
        'statusCode': 201,
        'body': 'Portfolio created'
    }

def updated_event(event):
    # Your logic here
    return {
        'statusCode': 200,
        'body': 'Portfolio updated'
    }
    
def deleted_event(event):
    # Your logic here
    return {
        'statusCode': 202,
        'body': 'Portfolio deleted'
    }
