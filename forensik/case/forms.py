from django.forms import forms
from forensik.case.models import Geodata


class MovieAdminForm(forms.ModelForm):

    class Meta:
        model = Geodata

    def save(self, commit=False):
        instance = super(MovieAdminForm, self).save(commit=commit)
        if not instance.pk and not self.current_user.is_superuser:
            if not self.current_user.profile.is_manager:
                instance.added_by = self.current_user.profile
        instance.save()
        return instance
