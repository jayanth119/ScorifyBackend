from rest_framework import serializers
from .models import MouldHumidity,VentilationItem,VentilationImages

class LandlordMouldSerializer(serializers.ModelSerializer):
    class Meta:
        model = MouldHumidity
        fields = "__all__"

class VentilationImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentilationImages
        fields ="__all__"

class VentilationItemSerializer(serializers.ModelSerializer):
    images = VentilationImagesSerializer(many=True,read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = VentilationItem
        fields = ['id','status','uploaded_images','images']
    
    def create(self,validated_data):
        images_data = validated_data.pop('uploaded_images')
        item = VentilationItem.objects.create(**validated_data)
        for image in images_data:
            VentilationImages.objects.create(item=item, image=image)
        return item
