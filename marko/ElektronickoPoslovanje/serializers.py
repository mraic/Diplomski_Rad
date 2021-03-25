from rest_framework import serializers
from .models import osobe

class osobeSerializer(serializers.ModelSerializer):
    class Meta:
        model = osobe
        fields = "__all__"
        