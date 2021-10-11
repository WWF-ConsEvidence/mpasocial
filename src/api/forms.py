from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from .models import MPAInterviewYear, UserProfile


class UserProfileForm(forms.ModelForm):
    mpa_interviewyears = forms.ModelMultipleChoiceField(
        queryset=MPAInterviewYear.objects.all().order_by("mpa__name", "year"),
        required=False,
        widget=FilteredSelectMultiple("MPAs / interview years", is_stacked=False),
        label="MPAs / interview years",
    )

    class Meta:
        model = UserProfile
        fields = ["mpa_interviewyears"]
