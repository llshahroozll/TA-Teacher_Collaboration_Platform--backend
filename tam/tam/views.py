from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def getRoute(request):
    route= [

        {'GET':'/user-profile-courses'},
        
        {'POST':'/login'},

    ]    
    
    return Response(route)