from django import forms
from django.utils.translation import gettext_lazy as _


class SignupForm(forms.Form):
    first_name = forms.CharField(
        label=_("First name"),
        max_length=124,
        widget=forms.TextInput(
            attrs={"placeholder": _("First name"), "autocomplete": "first_name"}
        ),
    )
    last_name = forms.CharField(
        label=_("Last name"),
        max_length=124,
        widget=forms.TextInput(
            attrs={"placeholder": _("Last name"), "autocomplete": "last_name"}
        ),
    )

    base_fields = ["first_name", "last_name"]

    def signup(self, request, user):
        """
        Invoked at signup time to complete the signup of the user.
        """
        pass
