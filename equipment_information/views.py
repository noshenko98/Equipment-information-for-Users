from tokenize import Comment

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from equipment_information.forms import ManufacturerSearchForm, EquipmentCategorySearchForm, UserUsernameSearchForm
from equipment_information.models import Manufacturer, Equipment, Commentary, EquipmentCategory, User


@login_required
def index(request):
    num_manufacturers = Manufacturer.objects.all().count()
    num_equipments = Equipment.objects.all().count()
    num_comments = Commentary.objects.all().count()
    count_visits = request.session.get("count_visits", 0)
    request.session["count_visits"] = count_visits + 1
    context = {
        "num_manufacturers": num_manufacturers,
        "num_equipments": num_equipments,
        "num_comments": num_comments,
        "count_visits": count_visits + 1,
    }
    return render(request,
                  "equipment_information/index.html",
                  context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "equipment_information/manufacturer_list.html"
    paginate_by=5

    def get_queryset(self):
        queryset = Manufacturer.objects.all()
        search_name = self.request.GET.get("name")
        if search_name:
            return queryset.filter(name__icontains=search_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ManufacturerListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ManufacturerSearchForm(
            initial={"name": name}
        )
        return context


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("equipment_information:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("equipment_information:manufacturer-list")


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("equipment_information:manufacturer-list")


class EquipmentCategoryListView(LoginRequiredMixin, generic.ListView):
    model = EquipmentCategory
    context_object_name = "equipment_category_list"
    template_name = "equipment_information/equipment_category_list.html"
    paginate_by = 2

    def get_queryset(self):
        queryset = EquipmentCategory.objects.all()
        search_name = self.request.GET.get("name")
        if search_name:
            return queryset.filter(name__icontains=search_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(EquipmentCategoryListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = EquipmentCategorySearchForm(
            initial={"name": name}
        )
        return context


class EquipmentCategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = EquipmentCategory
    fields = "__all__"
    success_url = reverse_lazy("equipment_information:equipments-category-list")
    template_name = "equipment_information/equipment_category_form.html"


class EquipmentCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = EquipmentCategory
    fields = "__all__"
    success_url = reverse_lazy("equipment_information:equipments-category-list")
    template_name = "equipment_information/equipment_category_form.html"


class EquipmentCategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = EquipmentCategory
    success_url = reverse_lazy("equipment_information:equipments-category-list")
    template_name = "equipment_information/equipment_category_confirm_delete.html"


class UserListView(LoginRequiredMixin, generic.ListView):
    model = User
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = UserUsernameSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.GET.get("username")
        if username:
            return queryset.filter(username__icontains=username)
        return queryset


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User

@login_required
def remove_from_favorites(request, pk_user, pk_equipment):
    if request.user.id == pk_user:
        equipment = Equipment.objects.get(pk=pk_equipment)
        request.user.favorite_equipment.remove(equipment)
    return HttpResponseRedirect(reverse_lazy("equipment_information:user-detail", args=[pk_user]))
