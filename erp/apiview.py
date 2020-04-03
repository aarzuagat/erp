from rest_framework import viewsets

from . import models, apiserializer


class CompanyConfiguration(viewsets.ModelViewSet):
    serializer_class = apiserializer.CCSerializer
    queryset = models.CompanyConfiguration.objects.all()
    lookup_field = 'pk'

    def post(self, request, format=None):
        print(request.data)
        x = 5

