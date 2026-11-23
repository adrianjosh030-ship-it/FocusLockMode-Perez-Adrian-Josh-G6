from django.urls import path
from . import views

app_name = "focus"
urlpatterns = [
    path("", views.session_list, name="list"),
    path("new/", views.session_create, name="create"),
    path("<int:pk>/", views.session_detail, name="detail"),
    path("<int:pk>/edit/", views.session_update, name="update"),
    path("<int:pk>/delete/", views.session_delete, name="delete"),
    path("<int:pk>/start/", views.session_start, name="start"),
    path("<int:pk>/finish/<str:outcome>/", views.session_finish, name="finish"),
        path("categories/new/", views.category_create, name="category_create"),
]
