from django.contrib import admin
from django.urls import path, include
from bookingsystem import views  # Impor fungsi dashboard dari views.py

urlpatterns = [
    path('admin/', admin.site.urls),          # Halaman admin
    path('api/', include('bookingsystem.urls')),  # Semua endpoint API
    path('', views.dashboard, name='dashboard'), # Path kosong diarahkan ke dashboard
]
