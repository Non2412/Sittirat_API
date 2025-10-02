def handler(request):
    return {
        'statusCode': 200,
        'body': {
            'message': 'Hello from Sittirat Tourism API!',
            'status': 'success',
            'endpoints': {
                '/api/tourist-attractions': 'Tourist attractions data',
                '/api/accommodations': 'Hotels and resorts data', 
                '/api/tour-packages': 'Tour packages data'
            }
        }
    }