from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin

from equipment_information.forms import (ManufacturerSearchForm,
                                         EquipmentCategorySearchForm,
                                         UserUsernameSearchForm,
                                         UserCreateForm,
                                         UserUpdateForm,
                                         EquipmentNameModelSearchForm, CommentaryForm)
from equipment_information.models import (Manufacturer,
                                          Equipment,
                                          Commentary,
                                          EquipmentCategory,
                                          User)


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
    if not request.GET.get("from"):
        return HttpResponseRedirect(reverse_lazy("equipment_information:user-detail", args=[pk_user]))
    return HttpResponseRedirect(reverse_lazy("equipment_information:equipment-detail", args=[pk_equipment]))



class UserCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = UserCreateForm
    success_url = reverse_lazy("equipment_information:user-list")


class UserUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("equipment_information:user-list")

    def test_func(self):
        user = self.get_object()
        return self.request.user == user or self.request.user.is_superuser


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy("equipment_information:user-list")

    def test_func(self):
        user = self.get_object()
        return self.request.user == user or self.request.user.is_superuser


class EquipmentListView(LoginRequiredMixin, generic.ListView):
    model = Equipment
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(
            EquipmentListView, self).get_context_data(**kwargs)
        search_query = self.request.GET.get("search_query", "")
        context["search_form"] = EquipmentNameModelSearchForm(
            initial={"search_query": search_query}
        )
        return context

    def get_queryset(self):
        queryset = Equipment.objects.select_related("manufacturer", "category").all()
        search_query = self.request.GET.get("search_query")
        if search_query:
            return queryset.filter(Q(name__icontains=search_query) | Q(model__icontains=search_query))
        return queryset


class EquipmentDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Equipment
    form_class = CommentaryForm
    queryset = Equipment.objects.all().select_related("manufacturer")

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.equipment_post = self.object
        comment.user = self.request.user
        comment.save()
        return redirect("equipment_information:equipment-detail", pk=self.object.pk)


@login_required
def add_to_favorites(request, pk_equipment):
    equipment = Equipment.objects.get(pk=pk_equipment)
    request.user.favorite_equipment.add(equipment)
    return HttpResponseRedirect(reverse_lazy("equipment_information:equipment-detail", args=[pk_equipment]))