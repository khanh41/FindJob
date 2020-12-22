from django import forms
from .models import *


class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['Email'].widget.attrs['placeholder'] = 'Enter a valid E-mail'

    class Meta:
        model = Contact
        fields = [
            'first_name',
            'last_name',
            'Email',
            'subject',
            'message'
        ]


class JobListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JobListingForm, self).__init__(*args, **kwargs)
        self.fields['job_location'].widget.attrs['placeholder'] = 'Da Nang, Viet Nam'
        self.fields['Salary'].widget.attrs['placeholder'] = '1k USD/month'
        self.fields['title'].widget.attrs['placeholder'] = 'Software Engineer, Web Designer'
        self.fields['application_deadline'].widget.attrs['placeholder'] = '2020-12-27'
        self.fields['title'].required = False
        self.fields['company_name'].required = False
        self.fields['employment_status'].required = False
        self.fields['vacancy'].required = False
        self.fields['gender'].required = False
        self.fields['category'].required = False
        self.fields['description'].required = False
        self.fields['responsibilities'].required = False
        self.fields['experience'].required = False
        self.fields['job_location'].required = False
        self.fields['Salary'].required = False
        self.fields['application_deadline'].required = False
        self.fields['published_on'].required = False
    class Meta:
        model = JobListing
        exclude = ('user', 'image')
        labels = {
            "job_location": "Job Location",
            "published_on": "Publish Date"
        }


class JobApplyForm(forms.ModelForm):
    class Meta:
        model = ApplyJob
        fields = '__all__'
        labels = {
            "file": "CV (pdf format)",
            "name": "Full Name"

        }
