from django.urls import path
from .views import UploadCSVView, DashboardView

urlpatterns = [
    path('upload/', UploadCSVView.as_view()),
    path('dashboard/', DashboardView.as_view()),
]