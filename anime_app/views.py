from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class GetRoutes(APIView):
    def get(self, request):
        routes = [
            {'GET': 'api/routes/'},
            {'POST': 'api/auth/login/'},
            {'POST': 'api/auth/refresh'},
        ]

        return Response(routes)