from django.urls import path
from meetings import views

urlpatterns = [
    path('', views.MeetingCreateView.as_view()),
    path('all/', views.MeetingListView.as_view()),
    path('<int:pk>/', views.UpdateDestroyMeetingView.as_view()),
    path('<int:pk>/', views.RetrieveMeetingView.as_view()),
]
