from rest_framework import serializers
from . import models


class CCSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CompanyConfiguration
        fields = '__all__'