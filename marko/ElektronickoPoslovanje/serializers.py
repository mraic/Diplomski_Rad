from rest_framework import serializers
from .models import *

class osobeSerializer(serializers.ModelSerializer):

    class Meta:

        model = osobe
        fields = "__all__"
        

class ulogeSerializer(serializers.ModelSerializer):

    class Meta: 

        model = uloga
        fields = '__all__'


class kolegijiSerializer(serializers.ModelSerializer):

    class Meta:

        model = kolegiji
        fields = '__all__'

class studijSerializer(serializers.ModelSerializer):

    class Meta:

        model = studij
        fields = '__all__'


class ucionicaSerializer(serializers.ModelSerializer):

    class Meta:

        model = ucionica
        fields = '__all__'



class terminiSerializer(serializers.ModelSerializer):

    class Meta:

        model = termini
        fields = '__all__'


class evidencijaSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = evidencija
        fields = '__all__'