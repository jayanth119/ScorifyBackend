from rest_framework import generics
from core.models import Landlord, Tenant, Agent , Property 
from core.LATserializer  import LandlordSerializer, TenantSerializer, AgentSerializer,PropertySerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from inventory_insception.models import  Inventory, Room, Condition
from django.core.files.storage import default_storage
import PyPDF2
import re
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
import json
import os 
from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from  .LATserializer  import TenantPropertyDashboardSerializer , LandlordPropertyDashboardSerializer
from .models import Property
# View to retrieve details of a Landlord by ID
class LandlordDetailView(generics.RetrieveAPIView):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer
    lookup_field = 'id'  # Use UUID field to look up the landlord

# View to retrieve details of a Tenant by ID
class TenantDetailView(generics.RetrieveAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    lookup_field = 'id'  # Use UUID field to look up the tenant

# View to retrieve details of an Agent by ID
class AgentDetailView(generics.RetrieveAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    lookup_field = 'id'  # Use UUID field to look up the agent

# View to list all Landlords
class LandlordListView(generics.ListAPIView):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer

# View to list all Tenants
class TenantListView(generics.ListAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

# View to list all Agents
class AgentListView(generics.ListAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

class PropertyDetailView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'id'  # Use UUID field to look up the property

# View to list all Properties
class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class LandlordReportUploadView(View):
    
    
    def extract_text_from_pdf(self, pdf_path):
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text

    def analyze_document(self, pdf_text):
        prompt = f"""
        Your task is to analyze the provided text from a property inventory report and follow these steps:

        Detect Room Name: Identify the name of the room described in the text.
        Identify Related Images: Detect all the images in the document that are related to the identified room.
        Gather Page Numbers: Collect the page numbers where these images are located.
        Repeat for Each Room: Continue this process for each room described in the document.

        Avoid Misclassification: If the images are not clearly associated with a particular room, do not include them in the results. Ensure that the output is accurate and does not include hallucinated or misconceived information.
        The text to analyze is:
            {pdf_text}
        Return in the following format:
            'Room name':'list of page numbers','Another room name':'list of page numbers'
        
        give only in the above mentioned format and nothing else follow it strictly.
        """

        # Non-streaming request
        client = OpenAI(api_key="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")

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        # Extract and return the JSON from the response
        return completion.choices[0].message.content.strip()

    def sanitize_folder_name(self, name):
        return re.sub(r'[\\/*?:"<>|]', "_", name)

    def extract_images_for_rooms(self, pdf_path, dic, property_id):
        pdf_document = fitz.open(pdf_path)
        main_folder = f"properties/{property_id}/"

        if not os.path.exists(main_folder):
            os.makedirs(main_folder)

        for room_name, pages in dic.items():
            sanitized_room_name = self.sanitize_folder_name(room_name)
            room_folder = os.path.join(main_folder, sanitized_room_name)
            if not os.path.exists(room_folder):
                os.makedirs(room_folder)

            for page_num in pages:
                page = pdf_document.load_page(page_num - 1)
                image_list = page.get_images(full=True)

                if image_list:
                    for img_index, img in enumerate(image_list):
                        xref = img[0]
                        base_image = pdf_document.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]

                        image = Image.open(BytesIO(image_bytes))

                        image_filename = f"{sanitized_room_name}_page_{page_num}_{img_index+1}.{image_ext}"
                        image_path = os.path.join(room_folder, image_filename)

                        image.save(image_path)
                        print(f"Saved image: {image_path}")
                else:
                    print(f"No images found on page {page_num} for room {sanitized_room_name}.")
    
    
    def post(self, request, landlord_uuid):
        landlord = get_object_or_404(Landlord, user__id=landlord_uuid)
        property_obj = landlord.properties.first()

        if not property_obj:
            return JsonResponse({'status': 'error', 'message': 'No properties associated with this landlord.'}, status=400)

        uploaded_file = request.FILES.get('report')
        if not uploaded_file:
            return JsonResponse({'status': 'error', 'message': 'No file uploaded.'}, status=400)

        file_path = default_storage.save(f'reports/{uploaded_file.name}', uploaded_file)

        pdf_text = self.extract_text_from_pdf(file_path)
        room_data = self.analyze_document(pdf_text)
        
        inspection = Inventory.objects.create(
            property=property_obj,
            document=file_path,
            score=0.0,
            date=request.POST.get('date'),
            type=request.POST.get('type'),
            title=request.POST.get('title'),
            created_by=request.user.username,
            expiry_date=request.POST.get('expiry_date'),
            past_inspection=False
        )

        for room_name, details in room_data.items():
            room, created = Room.objects.get_or_create(
                inspection=Inventory,
                name=room_name,
                defaults={'completion_percentage': 0.0}
            )

            for item in details.get('items', []):
                Condition.objects.create(
                    room=room,
                    item=item['name'],
                    condition=item['condition'],
                    document=None
                )

        self.extract_images_for_rooms(file_path, room_data, property_obj.id)

        return JsonResponse({'status': 'success', 'message': 'Report processed successfully'})


class TenantDashboardView(APIView):
    def get(self, request, tenant_id):
        # Assuming each tenant is associated with one primary property
        property = Property.objects.filter(tenants__id=tenant_id).first()
        if property:
            serializer = TenantPropertyDashboardSerializer(property)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Property not found for this tenant."}, status=status.HTTP_404_NOT_FOUND)
    

class LandlordDashboardView(APIView):
    def get(self, request, landlord_id):
        properties = Property.objects.filter(landlords__id=landlord_id)
        if properties.exists():
            serializer = LandlordPropertyDashboardSerializer(properties, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No properties found for this landlord."}, status=status.HTTP_404_NOT_FOUND)
