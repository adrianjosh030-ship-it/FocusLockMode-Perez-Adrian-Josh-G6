from django import forms
from .models import Category, FocusSession


class FocusSessionForm(forms.ModelForm):
    class Meta:
        model = FocusSession
        fields = ["title", "category", "planned_minutes", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user:
            self.fields["category"].queryset = Category.objects.filter(user=user)

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters.")
        return title

    def clean_planned_minutes(self):
        m = self.cleaned_data["planned_minutes"]
        if not 5 <= m <= 240:
            raise forms.ValidationError("Planned time must be between 5 and 240 minutes.")
        return m


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
