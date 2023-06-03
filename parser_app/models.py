from django.db import models
from django import forms
from django.forms import ClearableFileInput

# for deleting media files after record is deleted
from django.dispatch import receiver
from regex import T
import os.path


class job(models.Model):
    jobid = models.CharField('jobid', max_length=100, primary_key=True)
    jobrole = models.CharField('jobrole', max_length=100)
    jobdate = models.DateField('jobdate')
    jobexp = models.IntegerField(null=True, blank=True)
    joblocation = models.CharField('joblocation', max_length=100)
    jobdescription = models.FileField('jobdescription', upload_to='desc/')

    # class Meta:
    # db_table:"parser_app_job"

    # class Meta:
    # db_table = "job"


class Resume(models.Model):
    resume = models.FileField('Upload Resumes', upload_to='resumes/')
    name = models.CharField('Name', max_length=255, null=True, blank=True)
    email = models.CharField('Email', max_length=255, null=True, blank=True)
    jobs = models.CharField('jobs', max_length=255, null=True, blank=True)
    mobile_number = models.CharField(
        'Mobile Number',  max_length=255, null=True, blank=True)
    education = models.CharField(
        'Education', max_length=255, null=True, blank=True)
    skills = models.CharField('Skills', max_length=1000, null=True, blank=True)
    company_name = models.CharField(
        'Company Name', max_length=1000, null=True, blank=True)
    college_name = models.CharField(
        'College Name', max_length=1000, null=True, blank=True)
    designation = models.CharField(
        'Designation', max_length=1000, null=True, blank=True)
    experience = models.CharField(
        'Experience', max_length=1000, null=True, blank=True)
    uploaded_on = models.DateTimeField('Uploaded On', auto_now_add=True)
    total_experience = models.CharField(
        'Total Experience (in Years)', max_length=1000, null=True, blank=True)
    matchpercentage = models.CharField(
        'Match Percentage', max_length=1000, null=True, blank=True)
    res = models.TextField(null=True, blank=True)
    fullname = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    exp = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=100, null=False, blank=False)
    # jobid = models.ForeignKey(job, on_delete=models.CASCADE)
    matching = models.IntegerField(null=True, blank=True)
    short = models.IntegerField(null=True, blank=True)
    short2 = models.IntegerField(null=True, blank=True)


class applicants(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Name', max_length=255, null=True, blank=True)
    username = models.CharField(
        'Username', max_length=255, null=True, blank=True)
    email = models.CharField('Email', max_length=255, null=True, blank=True)
    mobile_number = models.CharField(
        'Mobile Number',  max_length=255, null=True, blank=True)
    password = models.CharField(
        'Password', max_length=255, null=True, blank=True)
    cpassword = models.CharField(
        'Confirm Password', max_length=255, null=True, blank=True)


class contactComment(models.Model):
    fullName = models.CharField('Full Name', max_length=100, blank=True)
    user_email = models.CharField(
        'Email', max_length=255, null=True, blank=True)
    comment = models.TextField(
        'Comment', max_length=65535, null=True, blank=True)


class recruiters(models.Model):
    FullName = models.CharField('Full Name', max_length=100, blank=True)
    recruiter_email = models.CharField(
        'Email', max_length=255, null=True, blank=True)
    username = models.CharField(
        'Username', max_length=100, null=True, blank=True)
    recruiter_password = models.CharField(
        'Password', max_length=20, null=True, blank=True)
    recruiter_confirm_password = models.CharField(
        'Confirm Password', max_length=20, null=True, blank=True)


class UploadResumeModelForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume']
        widgets = {
            'resume': ClearableFileInput(attrs={'multiple': True}),
        }
