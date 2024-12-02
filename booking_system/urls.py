from django.contrib import admin
from django.urls import path, include
from bookingsystem import views  # Impor fungsi dashboard dari views.py


urlpatterns = [
    path('admin/', admin.site.urls),           # URL admin
    path('api/', include('bookingsystem.urls')),  # URL API
    path('', views.dashboard, name='dashboard'),  # Root URL diarahkan ke dashboard
    path('dashboard/', views.dashboard, name='dashboard'),  # URL /dashboard diarahkan ke dashboard
]
