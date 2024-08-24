import os,random
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def profile_photo_upload_path(instance, filename):
    # Extracting the file extension
    ext = filename.split('.')[-1]
    
    # Creating the folder structure based on user type
    if instance.user.user_type == 'tenant':
        folder = 'tenant'
    elif instance.user.user_type == 'agent':
        folder = 'agent'
    elif instance.user.user_type == 'landlord':
        folder = 'landlord'
    
    # Constructing the filename as the user's UUID
    filename = f"{instance.user.id}.{ext}"
    
    # Full upload path
    return os.path.join('profilephotos', folder, filename)


class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='landlord_profile')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    properties = models.ManyToManyField('Property', related_name='landlords', blank=True)
    profile_photo = models.ImageField(upload_to=profile_photo_upload_path, null=True, blank=True)
    unique_code = models.CharField(max_length=6,unique=True,null=True,blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def generate_unique_code(self):
        while True:
            code = str(random.randint(100000, 999999))
            if not Landlord.objects.filter(unique_code=code).exists():
                return code


class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='tenant_profile')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    landlord = models.ForeignKey('Landlord', related_name='tenants', on_delete=models.CASCADE, null=True, blank=True)  
    properties = models.ManyToManyField('Property', related_name='tenants', blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    occupation = models.CharField(max_length=255, null=True, blank=True)  # Add this line

    is_verified = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to=profile_photo_upload_path, null=True, blank=True)

    def __str__(self):
        return self.name


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='agent_profile')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.CharField(max_length=255)
    website = models.URLField()
    landlords = models.ManyToManyField(Landlord, related_name='agents', blank=True)
    tenants = models.ManyToManyField(Tenant, related_name='agents', blank=True)
    profile_photo = models.ImageField(upload_to=profile_photo_upload_path, null=True, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=255)
    house_name = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    bathroom_count = models.IntegerField()
    living_room_count = models.IntegerField()
    property_type = models.CharField(max_length=50)
    house_age = models.IntegerField()
    floor_map_photos = models.TextField()
    epc_status = models.CharField(max_length=50)
    risk_assessment_percentage = models.FloatField()
    mould_ventilation_percentage = models.FloatField()
    gas_safety = models.BooleanField()
    heat_safety = models.BooleanField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    deposit = models.FloatField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    next_inspection_date = models.DateField(null=True, blank=True)
    open_repair_count = models.IntegerField(default=0)
    inspection_count = models.IntegerField(default=0)
    regular_maintenance = models.BooleanField(default=False)
    inventory_count = models.IntegerField(default=0)

    def __str__(self):
        return self.address


class Management(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    details = models.TextField()

    def __str__(self):
        return f'Management - {self.agent} - {self.property}'


class LettingManagement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    tenant_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='letting_managements')
    landlord_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='landlord_letting_managements')
    details = models.TextField()

    def __str__(self):
        return f'Letting Management - {self.agent} - {self.tenant_property.address}'


class SalesManagement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    landlord_property = models.ForeignKey(Property, on_delete=models.CASCADE)
    details = models.TextField()

    def __str__(self):
        return f'Sales Management - {self.agent} - {self.landlord_property.address}'


class PropertyTimeline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    date = models.DateField()
    maintenance_repair_type = models.CharField(max_length=50)
    performed_by = models.CharField(max_length=255)
    details = models.TextField()

    def __str__(self):
        return f'Timeline - {self.property} - {self.date}'
    

class HousePhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=255)

    def __str__(self):
        return f'Photo - {self.property} - {self.item_type}'

class HouseItemImages(models.Model):
    STATUS_CHOICES = (
        ('checkin', 'Check-in'),
        ('checkout', 'Checkout'),
        ('inspection', 'Inspection'),
        ('services', 'Services'),
    )
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES)
    item = models.ForeignKey(HousePhoto,on_delete=models.CASCADE,related_name='house_item')
    upload_date = models.DateField(auto_now=True)
    image = models.ImageField(upload_to='house_photos/')

    def __str__(self) -> str:
        return f' {self.item} {self.status} '