from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm




class ManufacturerSearchForm(forms.Form):
    name =forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by name",
        })
    )


class EquipmentCategorySearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by name",
        })
    )


class UserUsernameSearchForm(forms.Form):
    username = forms.CharField(max_length=150,
                               required=False,
                               label="",
                               widget=forms.TextInput(
                                   attrs={
                                       "placeholder":
                                           "Search by Username"}
                               )
                               )

class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["username","first_name", "last_name", "favorite_equipment"]
        widgets = {
            "favorite_equipment": forms.CheckboxSelectMultiple()
        }


class EquipmentNameModelSearchForm(forms.Form):
    search_query = forms.CharField(max_length=150,
                                   required=False,
                                   label="",
                                   widget=forms.TextInput(
                                       attrs={
                                           "placeholder":
                                               "Search by name or model",
                                       }))