
import json
from .serializers import MaintenanceServiceSerializer,MaintenanceScheduleSerailizer,AgentRepairSerializer,LandlordRepairSerializer,AgentMaintenanceSerializer,TenantRepairHistorySerializer,TenantMaintenanceScheduleSerializer
from rest_framework.views import APIView
from .models import Maintenance,Repair
from core.models import HouseItemImages , HousePhoto ,Tenant
from regularmaintaince.models import Repair
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.parsers import MultiPartParser,FormParser
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
import base64
import requests
import uuid
from  inventory_insception.models import Inspection , Condition 
Customuser = get_user_model()
class LandlordMaintenanceServiceHistory(APIView):
    def get(self,request,user_id):
       maintenance = Maintenance.objects.filter(user__id=user_id)
       serializer = MaintenanceServiceSerializer(maintenance,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)

class AgentMaintenanceView(APIView):
    def get(self,request,user_id):
       repair= Repair.objects.filter(user__id=user_id)
       serializer = AgentMaintenanceSerializer(repair,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)
    

class LandlordScheduleList(APIView):
    def get(self,request,user_id):
       maintenance = Maintenance.objects.filter(user__id=user_id)
       serializer = MaintenanceScheduleSerailizer(maintenance,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)

class TenantScheduleList(APIView):
    parser_classes = [MultiPartParser,FormParser]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
       maintenance = maintenance = Maintenance.objects.filter(user=request.user)
       serializer = MaintenanceScheduleSerailizer(maintenance,many=True)
       return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
       
        request.data['user'] = request.user.id
        serializer = TenantMaintenanceScheduleSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

# class LandlordUpcomingList(APIView):
#     def get(self,request):
#        maintenance = Maintenance.objects.filter(performed_by='landlord')
#        serializer = MaintenanceUpcomingSerializer(maintenance,many=True)
#        return Response(serializer.data,status=status.HTTP_200_OK)
    
class AgentOpenRepairView(APIView):
    def get(self,request,user_id):
        repair = Repair.objects.filter(user__id=user_id)
        serializer = AgentRepairSerializer(repair,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class LandlordRepairHistoryView(APIView):
    def get(self,request,user_id):
        repairs = Repair.objects.filter(user__id=user_id)
        if repairs.exists():
            serializer = LandlordRepairSerializer(repairs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No repairs found for this user."}, status=status.HTTP_404_NOT_FOUND)

class TenantRepairHistoryView(APIView):
    def get(self,request):
        repairs = Repair.objects.filter(user=request.user)
        if repairs.exists():
            serializer = TenantRepairHistorySerializer(repairs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No repairs found for this user."}, status=status.HTTP_404_NOT_FOUND)

class TenantInspectionView(APIView):
    def post(self, request):
        tenant = Tenant.objects.get(user_id=request.user)
        property_id = request.data.get('property_id')
        item_type = request.data.get('item_type')
        ar = request.data.get('condition')
        room_id = request.data.get('room_id')
        
        # Check if the image is being uploaded as a file
        image_file = request.FILES.get('image')  # Image uploaded as a file
        
        if not image_file:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Convert the uploaded file to a base64 string (in case you need it)
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Describe the image (this should be adapted based on how you process images)
        image_description = "The image is of a {} with the following notable features...".format(item_type)
        
        # Call OpenAI API to analyze the image description
        analysis_result = self.analyze_item(item_type, ar, image_description)
        
        # Debugging: Inspect the API response
        print("Analysis Result:", analysis_result)
        
        # Check if the expected keys exist in the response
        if 'object_name' in analysis_result and 'object_rating' in analysis_result:
            if analysis_result['object_name'] == 'yes' and analysis_result['object_rating'] == 'yes':
                # Save the photo
                house_photo = HousePhoto.objects.create(property_id=property_id, item_type=item_type)
                saved_image = HouseItemImages.objects.create(
                    item=house_photo,
                    status='inspection',
                    image=self.decode_image(image_base64)
                )
                
                # Mark the condition as inspected
                condition = Condition.objects.get(room_id=room_id, item=item_type)
                Inspection.objects.create(
                    room_id=room_id,
                    condition=condition,
                    score=100,  # Assign a score based on your logic
                    is_completed=True,
                    notes=f"Inspection of {item_type} is complete and matches the expected condition."
                )
                
                # Check if all items in the room have been inspected
                if self.all_items_inspected(room_id):
                    inspection_status = "Inspection complete for room"
                else:
                    inspection_status = "Inspection successful, pending more items"

                return Response({
                    "status": inspection_status,
                    "item_type": item_type,
                    "condition": ar,
                    "image_url": saved_image.image.url
                }, status=status.HTTP_200_OK)
            elif analysis_result['object_rating'] == 'Repair':
                # Handle the case where the item needs repair
                repair = Repair.objects.create(
                    user=tenant.user,
                    property_id=property_id,
                    repair_score=0.0,  # You can modify this score based on your logic
                    repair_history=f"Repair needed for {item_type}",
                    status='pending',
                    description=f"Inspection indicates that {item_type} needs repair.",
                    completion_report="Pending",
                    cost=0.0,  # Update this with the actual repair cost if available
                    reported_by=tenant.name
                )
                
                return Response({
                    "status": "Repair needed",
                    "item_type": item_type,
                    "condition": ar,
                    "repair_status": "Repair record created",
                    "repair_id": repair.id  # Returning the repair ID might be useful for tracking
                }, status=status.HTTP_200_OK)
            else:
                # Handle the case where the object does not match or the rating is not 'yes'
                return Response({
                    "status": "Inspection did not match expectations",
                    "item_type": item_type,
                    "condition": ar,
                    "analysis_result": analysis_result  # Include the analysis result for debugging
                }, status=status.HTTP_200_OK)
        else:
            # Handle the case where the expected keys are missing
            return Response({"error": "Unexpected response from analysis", "debug": analysis_result}, status=status.HTTP_400_BAD_REQUEST)

      # Define the OpenAI API key and headers
    def analyze_item(self, itemname, ar, description):
        # Define the OpenAI API key and headers
        api_key ="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"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Construct the prompt with the description
        prompt = f"""
        You are an assistant tasked with analyzing a description of a '{itemname}' to determine its condition.
        The description is as follows: '{description}'.
        The possible conditions are only 'Good', 'Fair', or 'Repair'.
        
        Based on this description, please perform the following tasks:
        1. Identify whether the object is the same or similar to '{itemname}'. Return 'yes' or 'no'.
        2. Rate the '{itemname}' in one of the following categories:
        - Good: If the '{itemname}' is fully perfect.
        - Fair: If the '{itemname}' has some notable defects but is still functional.
        - Repair: If the '{itemname}' has defects like cracks, breakage, or other forms of damage that require repair.
        Compare the rating with the user's provided condition '{ar}'. If they match, return 'yes'. Otherwise, return 'no' and provide an explanation.

        Return the results in JSON format:
        - '{itemname}': Yes or no
        - If '{itemname}' is no: provide a description of the discrepancy.
        - '{itemname} rating': Yes or no
        - If '{itemname} rating' is no: provide an explanation.
        """

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        if 'choices' in response.json():
            json_content = response.json()['choices'][0]['message']['content']
            return json.loads(json_content)
        else:
            return {"error": "Analysis failed", "details": response.text}

    def decode_image(self, image_base64):
        image_data = base64.b64decode(image_base64)
        file_name = f'{uuid.uuid4()}.jpeg'
        return ContentFile(image_data, name=file_name)
    
    def all_items_inspected(self, room_id):
        conditions = Condition.objects.filter(room_id=room_id)
        for condition in conditions:
            if not Inspection.objects.filter(room_id=room_id, condition=condition, is_completed=True).exists():
                return False
        return True