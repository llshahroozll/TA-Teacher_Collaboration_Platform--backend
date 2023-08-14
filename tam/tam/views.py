from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_route(request):
    route= [

        {'GET':'/user-profile-courses'},
        {'GET':'/course/:id'},
        
        {'POST':'/login'},
        {'POST':'/update-profile'},
        
        

    ]    
    
    return Response(route)