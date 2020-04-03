from django.shortcuts import render
from django.http import JsonResponse
from . import models
from django.shortcuts import get_object_or_404

def test(request):
    file = request.FILES.get('file')
    id = request.POST.get('id')
    config = get_object_or_404(models.CompanyConfiguration, id=id)
    config.logo = file
    config.save()
    return JsonResponse({'uploaded':True})