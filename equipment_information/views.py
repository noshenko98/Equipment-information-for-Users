from tokenize import Comment

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from equipment_information.forms import ManufacturerSearchForm
from equipment_information.models import Manufacturer, Equipment, Commentary


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
    model=Manufacturer
    context_object_name="manufacturer_list"
    template_name="equipment_information/manufacturer_list.html"
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