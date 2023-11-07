from rest_framework import serializers
from .models import AweberCredentials

class AweberCredentialsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AweberCredentials
        fields = '__all__'

