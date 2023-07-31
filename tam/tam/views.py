from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def getRoute(request):
    route= [
        {'GET':'/courses'},
        {'GET':'/course'},
        {'GET':'/profiles'},
        {'GET':'/profile'},
        
        {'POST':'/login'},
        {'POST':'/login/refresh'},
    ]    
    
    return Response(route)