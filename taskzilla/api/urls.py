from django.urls import path
from . import views

urlpatterns = [
     path("goals/", views.GoalListCreate.as_view(), name = "goal-list"),
     path("goals/delete/<int:pk>", views.GoalDelete.as_view(), name = "delete-goal")
]
