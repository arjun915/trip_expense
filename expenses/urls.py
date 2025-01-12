# expenses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.trip_list, name='trip_list'),
    path('create/', views.create_trip, name='create_trip'),
    path('<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('<int:trip_id>/add_expense/', views.add_expense, name='add_expense'),
    path('trip/<int:trip_id>/summary/', views.trip_summary, name='trip_summary'),
    path('trip/<int:trip_id>/add_participant/', views.add_participant, name='add_participant'),
]
