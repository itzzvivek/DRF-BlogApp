from django.urls import path
from . import views

urlpatterns = [
    path("category_list/", views.CategoryListCreateView.as_view(), name="category_list"),
]
