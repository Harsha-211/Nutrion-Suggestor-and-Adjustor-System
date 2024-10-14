from .views import nutrition_analysis
from django.urls import path

urlpatterns = [
    path('', nutrition_analysis, name='nutrition_analysis'),
]
