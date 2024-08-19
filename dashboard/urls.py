from django.urls import path
from .views import dashboardData

urlpatterns = [
    path('dashboard/', dashboardData, name='dashboard-data'),
]
