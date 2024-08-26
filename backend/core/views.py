from django.conf import settings
from rest_framework import generics
from core.models import HouseItemImages, Landlord, Tenant, Agent , Property ,HousePhoto
from core.LATserializer  import LandlordSerializer, TenantSerializer, AgentSerializer,PropertySerializer,HousePhotoSerializer,TenantPropertyDashboardSerializer , LandlordPropertyDashboardSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from regularmaintaince.models import Maintenance
from inventory_insception.models import  Inventory, Room, Condition
from django.core.files.storage import default_storage
from PIL import Image
from io import BytesIO
import json,os,PyPDF2,re,fitz
from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics,permissions
from rest_framework.parsers import MultiPartParser, FormParser
from regularmaintaince.models import Repair
from django.db.models import Max

client = OpenAI(api_key="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")

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


class LandlordReportUploadView(APIView):

    def split_text_into_chunks(self, text, max_tokens=2000):
        # Splits text into smaller chunks of max_tokens length
        words = text.split()
        chunks = []
        current_chunk = []

        for word in words:
            if len(" ".join(current_chunk)) + len(word) + 1 > max_tokens:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
            current_chunk.append(word)
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks

    def extract_text_from_pdf(self, pdf_path):
        try:
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
        except FileNotFoundError:
            print(f"File not found: {pdf_path}")
            return None

    def analyze_document(self , pdf_text):
        # Define the prompt based on the refined instructions
        prompt = f"""
        You are a highly capable assistant tasked with extracting detailed room information from an inventory report. Your objectives are:

        1. Identify and list each room by name.
        2. Extract the contents within each room such as furniture, fixtures, appliances, and other items.    
        Return in json format for each room with room name and item name.Follow the below format only:
        room_name: [item_name1, item_name2, ...]...

    Follow only the Above mentionded format and nothing else.
        The document content is as follows:
        {pdf_text}
        """

        # Non-streaming request
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        # Extract and return the JSON from the response
        return completion.choices[0].message.content.strip()

    def analyze_document_for_images(self, pdf_text):
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
            "Room name": "list of page numbers", "Another room name": "list of page numbers"

        Give only in the above-mentioned format and nothing else. Follow it strictly.
        """

        # Non-streaming request
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
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
                # Ensure page_num is an integer
                try:
                    page_num = int(page_num)
                except ValueError:
                    print(f"Invalid page number: {page_num} for room {sanitized_room_name}. Skipping...")
                    continue

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
                        house_photo = HousePhoto.objects.create(property_id=property_id, item_type=sanitized_room_name)
                        HouseItemImages.objects.create(
                            item=house_photo,
                            status='checkin',
                            image=image_path
                        )
                        print(f"Saved image: {image_path}")
                else:
                    print(f"No images found on page {page_num} for room {sanitized_room_name}.")

    def post(self, request, landlord_uuid):
        landlord = get_object_or_404(Landlord, user__id=landlord_uuid)
        property_obj = landlord.properties.first()

        if not property_obj:
            return Response({'status': 'error', 'message': 'No properties associated with this landlord.'}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.FILES.get('report')
        if not uploaded_file:
            return Response({'status': 'error', 'message': 'No file uploaded.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Temporarily save the file to process it
        temp_file_path = f'temp_{uploaded_file.name}'
        with default_storage.open(temp_file_path, 'wb+') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        full_temp_file_path = os.path.join(settings.MEDIA_ROOT, temp_file_path)

        # Extract text from the PDF
        pdf_text = self.extract_text_from_pdf(full_temp_file_path)
        if pdf_text is None:
            return Response({'status': 'error', 'message': 'Failed to extract text from the PDF.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Analyze the document
        json_output = self.analyze_document_for_images(pdf_text)
        
        # Clean the output if necessary
        if "```" in json_output:
            json_output = json_output.replace("```", "")
        
        # Ensure the string is formatted properly as a JSON string
        formatted_str = "{" + json_output + "}"
        formatted_str = formatted_str.replace("'", "\"")
        print(formatted_str)
        try:
            room_data = json.loads(formatted_str)  # Convert JSON string to dictionary
        except json.JSONDecodeError as e:
            return Response({'status': 'error', 'message': f'Failed to parse JSON: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Process room data
        json_output = self.analyze_document(pdf_text)
        l=["```","json"]
        for i in l:
            if(i in json_output):
                json_output=json_output.replace(i,"")
        room_data = json.loads(json_output)
        # Print the JSON output
        # dicc = json.dumps(room_data, indent=4)
        print(room_data.items())

        # Save the file after processing the data
        final_file_path = default_storage.save(f'reports/{uploaded_file.name}', uploaded_file)
        full_final_file_path = os.path.join(settings.MEDIA_ROOT, final_file_path)

        # Create Inventory object
        inspection = Inventory.objects.create(
            property=property_obj,
            document=final_file_path,
            score=0.0,
            date=request.data.get('date'),
            type=request.data.get('type'),
            title=request.data.get('title'),
            created_by=request.user.username,
            expiry_date=request.data.get('expiry_date'),
            past_inventory=request.data.get('past_inventory', False)  # Provide a default value if not supplied
        )

        for room_name, pages in room_data.items():
            room, created = Room.objects.get_or_create(
                inventory=inspection,
                name=room_name,
                defaults={'completion_percentage': 69.00}
            )

            licst = room_data[room_name] 
            for i in licst :
                item , created = Condition.objects.get_or_create(
                    room = room , 
                    item = i 
                )
        self.extract_images_for_rooms(full_final_file_path, room_data, property_obj.id)

        # Clean up temporary file
        default_storage.delete(temp_file_path)

        return Response({'status': 'success', 'message': 'File uploaded and processed successfully.'}, status=status.HTTP_201_CREATED)


class TenantDashboardView(APIView):
    permission_classes =[permissions.IsAuthenticated]
    def get(self, request):
        try:
            tenant = Tenant.objects.get(user=request.user)
            properties = tenant.properties.all()
            repair = Repair.objects.filter(user=tenant.user).count()
            house_photo_count =0
            property_data = []
            for obj in properties:
                count = HouseItemImages.objects.filter(item__property=obj).count()
                house_photo_count+=count
                maintenace_count = Maintenance.objects.filter(property=obj).count()
                last_due_date = Maintenance.objects.filter(property=obj).aggregate(Max('due_date'))['due_date__max']
                
                property_data.append({
                    'last_due_date': last_due_date,
                    'maintenance_count':maintenace_count
                })
            if properties:
                serializer = TenantPropertyDashboardSerializer(properties, many=True)
                data = {
                    'properties': serializer.data,
                    'repair_count': repair,
                    'inspection':properties.count(),
                    'house_photos':house_photo_count,
                    'heat_system_status':'Good',
                    'heat_system_safety':'Good',
                    'maintenance':property_data
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Property not found for this tenant."}, status=status.HTTP_404_NOT_FOUND)
        
        except Tenant.DoesNotExist:
            return Response({"detail": "Tenant not found."}, status=status.HTTP_404_NOT_FOUND)


class LandlordDashboardView(APIView):
    def get(self, request, landlord_id):
        properties = Property.objects.filter(landlords__id=landlord_id)
        if properties.exists():
            serializer = LandlordPropertyDashboardSerializer(properties, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No properties found for this landlord."}, status=status.HTTP_404_NOT_FOUND)

class HousePhotoView(APIView):
    parser_classes = [MultiPartParser,FormParser]
    def get(self, request, *args, **kwargs):
        house_photos = HousePhoto.objects.all()
        serializer = HousePhotoSerializer(house_photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        property_id = kwargs.get('property_id')
        try :
            instance = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)
        request_data = request.data.copy()
        request_data['property'] = instance.id
        serializer = HousePhotoSerializer(data=request_data)
        if serializer.is_valid():
            house_photo = serializer.save()
            return Response(HousePhotoSerializer(house_photo).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)