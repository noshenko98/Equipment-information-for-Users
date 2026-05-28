"""
URL configuration for equipment_information_for_users project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path


from equipment_information.views import (index,ManufacturerListView,
                                         ManufacturerCreateView,
                                         ManufacturerUpdateView,
                                         ManufacturerDeleteView,
                                         EquipmentCategoryListView,
                                         EquipmentCategoryCreateView,
                                         EquipmentCategoryUpdateView,
                                         EquipmentCategoryDeleteView,
                                         UserListView,
                                         UserDetailView,
                                         remove_from_favorites)

urlpatterns = [
    path("", index, name="index"),
    path("manufacturers/", ManufacturerListView.as_view(),
         name="manufacturer-list"),
    path("manufacturers/create/",ManufacturerCreateView.as_view(),
         name="manufacturer-create"),
    path("manufacturers/<int:pk>/update/", ManufacturerUpdateView.as_view(),
         name="manufacturer-update"),
    path("manufacturers/<int:pk>/delete/", ManufacturerDeleteView.as_view(),
         name="manufacturer-delete"),
    path("equipments-category/", EquipmentCategoryListView.as_view(),
         name="equipments-category-list"),
    path("equipments-category/create/", EquipmentCategoryCreateView.as_view(),
         name="equipments-category-create"),
    path("equipments-category/<int:pk>/update/", EquipmentCategoryUpdateView.as_view(),
         name="equipments-category-update"),
    path("equipments-category/<int:pk>/delete/", EquipmentCategoryDeleteView.as_view(),
         name="equipments-category-delete"),
    path("users/", UserListView.as_view(),
         name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(),
         name="user-detail"),
    path("users/<int:pk_user>/remove-favorites/<int:pk_equipment>", remove_from_favorites,
        name="remove-favorites"),

]

app_name = "equipment_information"