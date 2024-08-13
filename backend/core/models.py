from django.db import models
import uuid

class Landlord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    properties = models.ManyToManyField('Property', related_name='landlords', blank=True)

    def __str__(self):
        return self.name

class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    current_tenancy_score = models.FloatField()
    landlord = models.ForeignKey(Landlord, related_name='tenants', on_delete=models.CASCADE)
    properties = models.ManyToManyField('Property', related_name='tenants', blank=True)

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

class Agent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.CharField(max_length=255)
    website = models.URLField()
    landlords = models.ManyToManyField(Landlord, related_name='agents', blank=True)
    tenants = models.ManyToManyField(Tenant, related_name='agents', blank=True)

    def __str__(self):
        return self.name


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
    name = models.CharField(max_length=255)
    photo = models.TextField()
    photo_type = models.CharField(max_length=50)
    uploaded_date = models.DateField()

    def __str__(self):
        return f'Photo - {self.property} - {self.photo_type}'
