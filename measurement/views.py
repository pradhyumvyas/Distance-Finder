from django.shortcuts import render, get_object_or_404
from .models import Measurement

# Create your views here.


def calculateDistanceView(request):
    obj = get_object_or_404(Measurement, id=1)

    context = {
        'distance':obj,
    }

    return render(request, 'measurement/main.html', context)