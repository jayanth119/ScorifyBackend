from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .serializers import LandlordMouldSerializer,VentilationItemSerializer,TenantMouldSerializer
from .models import MouldHumidity,VentilationItem
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
class LandlordMouldView(APIView):
    def get(self,request,uuid_id):
        mould = MouldHumidity.objects.filter(user__id=uuid_id)
        if mould.exists():
            serializer = LandlordMouldSerializer(mould,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"detail":"No Mould for this user"},status=status.HTTP_404_NOT_FOUND)

class VentilationItemView(ListCreateAPIView):
    queryset = VentilationItem.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = VentilationItemSerializer
    permission_classes = [permissions.IsAuthenticated]  
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TenantMouldView(APIView):
    def get(self,request):
        mould = MouldHumidity.objects.filter(user=request.user)
        if mould.exists():
            serializer = TenantMouldSerializer(mould,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"detail":"No Mould for this user"},status=status.HTTP_404_NOT_FOUND)
