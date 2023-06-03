from django import forms
from .models import job
from .models import recruiters


class DocumentForm(forms.ModelForm):
    class Meta:
        model = job
        fields = ('jobid', 'jobrole', 'jobdate',
                  'jobexp','joblocation','jobdescription')
class UserForm(forms.ModelForm):
    class Meta:
        model = recruiters
        fields = ('FullName', 'recruiter_email', 'username',
                  'recruiter_password','recruiter_confirm_password')
        widgets = {
        'recruiter_password': forms.PasswordInput(),
        'recruiter_confirm_password': forms.PasswordInput(),
    }
