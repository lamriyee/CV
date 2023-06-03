from matplotlib.style import context
from resume_parser.settings import BASE_DIR
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render, redirect
from pyresparser import ResumeParser
from .models import Resume, UploadResumeModelForm, job, applicants
from .forms import DocumentForm
from parser_app.models import job
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect, render
from .models import *
import pandas as pd
from numpy import *
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn import linear_model
from sklearn.tree import export_graphviz
from sklearn.tree import DecisionTreeClassifier
from sklearn import linear_model
from sklearn.metrics import accuracy_score, confusion_matrix
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse, Http404
import os.path
import shutil
from sys import argv
import docx2txt
import PyPDF2
from rest_framework import serializers
from django.core import serializers
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class train_model:

    def train(Category,resume):
        data = pd.read_csv('resume_parser/jobSkills.csv')
        array = data.values

        y = data['Category']
        print(y)

        X['Category'].values
        X['Resume'].values

        mul_lr = linear_model.LogisticRegression(
            multi_class='multinomial', solver='newton-cg', max_iter=1000)
        np.where(X.values >= np.finfo(np.float32).max)
        X = X.fillna(X.mean())
        mul_lr.fit(X, y)
        X_train = X
        y_train = y
        print(X_train.shape, y_train.size)
        dt2 = DecisionTreeClassifier(criterion='entropy')
        dt2.fit(X_train, y_train)
        X_train
        testdata = pd.read_csv('resume_parser/jobTest.csv')
        print(testdata.columns)
        drop_columns = ['Category']
        X_test = testdata.drop(drop_columns, axis=1)
        y_test = testdata['Category']
        y_pred = mul_lr.predict(X_test)
        y_pred
        y_pred_dt = dt2.predict(X_test)
        y_pred_dt
        dt_score = dt2.score(X_test, y_test)
        print(f"Decision Tree Classifier Accuracy score is {dt_score}")
        cm=confusion_matrix(y_test, y_test)
        normed_c = (cm.T / cm.astype(np.float).sum(axis=1)).T
        print("confusion matrix", normed_c)
        print(dt_score)
        dot_data = export_graphviz(dt2, out_file=None)
        print(dot_data)

        test = pd.DataFrame({'Category': Category, 'Resume': Category}, index=[0])
        print(mul_lr.predict(test))

        return mul_lr.predict(test)

    def test(self, test_data):
        try:
            test_predict = list()
            for i in test_data:
                test_predict.append(int(i))
            y_pred = self.mul_lr.predict(int([test_predict]))
            return y_pred
        except:
            print("All Factors For Finding Personality Not Entered!")

def prediction_result(aplcnt_name, personality_values):
    "after applying a job"
    applicant_data = {"Candidate Name": aplcnt_name,}
    age = personality_values[1]
    print("\n Candidate Entered Data \n")
    print(personality_values)
    personality = train_model()
    personality.test(personality_values)
    personality = train_model.test(personality_values)
    print("\n Predicted Personality \n")
    print(personality)
    return personality


def new(request, id):
    jb = job.objects.filter(jobid=id).first()
    print(id)
    file_form = UploadResumeModelForm(request.POST, request.FILES)
    files = request.FILES.getlist('resume')
    resumes_data = []
    if file_form.is_valid():
        for file in files:
            # saving the file
            resume = Resume(resume=file)
            resume.jobs = request.POST['jobs']
            resume.save()

            # extracting resume entities
            parser = ResumeParser(os.path.join(
                settings.MEDIA_ROOT, resume.resume.name))

            data = parser.get_extracted_data()
            resumes_data.append(data)
            resume.name = data.get('name')
            resume.email = data.get('email')
            resume.mobile_number = data.get('mobile_number')
            if data.get('degree') is not None:
                resume.education = ', '.join(data.get('degree'))
            else:
                resume.education = None
            resume.company_name = data.get('company_name')
            resume.college_name = data.get('college_name')
            resume.designation = data.get('designation')
            resume.total_experience = data.get('total_experience')
            if data.get('skills') is not None:
                resume.skills = ', '.join(data.get('skills'))
            else:
                resume.skills = None
            if data.get('experience') is not None:
                resume.experience = ', '.join(data.get('experience'))
            else:
                resume.experience = None
            jobsss = request.POST.get('jobsss')
            jobss = docx2txt.process(os.path.join(settings.MEDIA_ROOT,jobsss))

            resume.res = docx2txt.process(
                os.path.join(
                    settings.MEDIA_ROOT, resume.resume.name))

            text = [resume.res, jobss]

            cv = CountVectorizer(lowercase=False)
            count_matrix = cv.fit_transform(text)

            print('Similarity score : ',
                  cosine_similarity(count_matrix))

            matchpercentage = cosine_similarity(count_matrix)[0][1]
            resume.matchpercentage = round(matchpercentage*100, 2)

            if resume.matchpercentage >= 50:
                resume.short=1
            else:
                resume.short=0
            
            print('Your Resume {} % match to the job description !'.format(
                resume.matchpercentage))
            
            model = train_model()
            
            expr = request.POST['expr']

            # if expper >= 100:
            #     expper = 100

            # print(expper)

            resume.matching =double(resume.matchpercentage)
            if resume.matching >= 100:
                resume.matching = 100
            resume.save()

            return redirect('thankyou')


def home(request, jobid):
    return render(request, jobid, 'main.html')


@login_required(login_url='adlogin_page')
def adminhome(request):
    user = User.objects.all()
    user = request.user.username
    form = job.objects.all()

    return render(request, 'adminhome.html', {'user': user, 'form': form})


def thankyou(request):
    return render(request, 'thankyou.html')


def index(request):
    return render(request, 'signup.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if applicants.objects.filter(username=username).exists():
                messages.info(
                    request, 'This username already exists. Please try again!!')
                return redirect('index')
            elif applicants.objects.filter(email=email).exists():
                messages.info(request,'This email address already exist. Please try again!!')
                return redirect('index')
            else:
                users = applicants(
                    name=name, email=email, username=username,mobile_number=mobile_number, password=password, cpassword=cpassword)
                users.save()
                messages.info(
                    request, 'Account created successfully.')
                return redirect('login_page')
        else:
            messages.info(
                request, 'The Passwords doesnot match. Please try again!!')
            return redirect('index')
    else:
        return redirect('index')


def login_page(request):
    return render(request, 'login.html')

def check_status(request):
    return render(request, 'view_status.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if applicants.objects.filter(username=username).exists() and applicants.objects.filter(password=password).exists():
            return redirect('availablejobs')
        
        else:
            messages.info(request, 'Username or password incorrect!, Please try again')
            return redirect('login_page')
    else:
        return redirect('login_page')


def adlogin_page(request):
    return render(request, 'adminlogin.html')

def recruiterlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if recruiters.objects.filter(username=username).exists() and recruiters.objects.filter(recruiter_password=password).exists():
            return redirect('adminPage')
        else:
            messages.info(request, 'Username or password incorrect!, Please try again')
            return redirect('adlogin_page')
    else:
        return redirect('adlogin_page')
    
def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('adminPage')
        else:
            messages.info(request, 'Usename or password incorrect, Please try again')
            return redirect('adlogin_page')
    else:
        return redirect('adlogin_page')


def mainhome(request):
    return render(request, 'homepage.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def availablejobs(request):
    form = job.objects.all()
    return render(request, 'availablejobs.html', {'form': form})


def apply(request, id):
    jb = job.objects.get(jobid=id)
    return render(request, 'main.html', {'jb': jb})


def gallery(request):
    return render(request, 'gallery.html')


@login_required(login_url='adlogin_page')
def addjob(request):
    return render(request, 'addnewjob.html')


@login_required(login_url='adlogin_page')
def newjob(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job details added successfully')
    else:
        form = DocumentForm()
    return render(request, 'addnewjob.html', {
        'form': form
    })


@login_required(login_url='adlogin_page')
def viewapplicants(request):
    resumes = Resume.objects.all()
    return render(request, 'viewapplicants.html', {'resumes': resumes})

@login_required(login_url='adlogin_page')
def viewjobs(request):
    jobb = job.objects.all()
    return render(request, 'view_jobs.html', {'jobs': jobb})


@login_required(login_url='adlogin_page')
def pyresults(request):
    resumes = Resume.objects.filter(
        jobs='Python Developer') & Resume.objects.filter(short=1)
    return render(request, 'results.html', {'resumes': resumes})


@login_required(login_url='adlogin_page')
def jvresults(request):
    resumes = Resume.objects.filter(
        jobs='Java Developer') & Resume.objects.filter(short=1)
    return render(request, 'results.html', {'resumes': resumes})


@login_required(login_url='adlogin_page')
def trresults(request):
    resumes = Resume.objects.filter(
        jobs='Trainer') & Resume.objects.filter(short=1)
    return render(request, 'results.html', {'resumes': resumes})


@login_required(login_url='adlogin_page')
def teresults(request):
    resumes = Resume.objects.filter(
        jobs='Technician') & Resume.objects.filter(short=1)
    return render(request, 'results.html', {'resumes': resumes})


@login_required(login_url='adlogin_page')
def hrresults(request):
    resumes = Resume.objects.filter(
        jobs='HR Excecutive') & Resume.objects.filter(short=1)
    return render(request, 'results.html', {'resumes': resumes})


@login_required(login_url='adlogin_page')
def manresults(request):
    resumes = Resume.objects.filter(
        jobs='Sales Manager') & Resume.objects.filter(short=1)
    return render(request, 'results.html', {'resumes': resumes})


def logout(request):
    request.session["uid"] = ""
    auth.logout(request)
    return redirect('/')

def adminlogout(request):
    request.session["uid"] = ""
    auth.logout(request)
    return redirect('adlogin_page')

@login_required(login_url='adlogin_page')
def adminPage(request):
    resumes = Resume.objects.all()
    applicants_count=resumes.count()
    jobo=job.objects.all()
    job_count=jobo.count()

    total_users=applicants.objects.all()
    users_count=total_users.count()

    commments=serializers.serialize('python',contactComment.objects.all())

    users_comment=contactComment.objects.all()
    comment_count=users_comment.count()

    application_request=serializers.serialize('python',Resume.objects.all())
    
    applied_users=Resume.objects.all()
    application_count=applied_users.count()

    context = {
        'resumes' : resumes,
        'applicants_count' :applicants_count,
        'jobo' : jobo,
        'job_count' : job_count,
        'total_users' : total_users,
        'users_count' : users_count,
        'commments' : commments,
        'users_comment' : users_comment,
        'comment_count' :comment_count,
        'application_request' : application_request,
        'applied_users' : applied_users,
        'application_count' : application_count
    }
    return render(request,"HR_page.html",context)

@login_required(login_url='adlogin_page')
def viewjobs(request):
    joboo=serializers.serialize('python',job.objects.all())

    resumes = Resume.objects.all()
    applicants_count=resumes.count()
    jobo=job.objects.all()
    job_count=jobo.count()

    total_users=applicants.objects.all()
    users_count=total_users.count()

    commments=serializers.serialize('python',contactComment.objects.all())

    users_comment=contactComment.objects.all()
    comment_count=users_comment.count()

    application_request=serializers.serialize('python',Resume.objects.all())
    
    applied_users=Resume.objects.all()
    application_count=applied_users.count()
    context = {
        'joboo' :joboo,
        'resumes' : resumes,
        'applicants_count' :applicants_count,
        'jobo' : jobo,
        'job_count' : job_count,
        'total_users' : total_users,
        'users_count' : users_count,
        'commments' : commments,
        'users_comment' : users_comment,
        'comment_count' :comment_count,
        'application_request' : application_request,
        'applied_users' : applied_users,
        'application_count' : application_count
    }

    return render(request,"viewjobs.html",context)
def writeComment(request):
    if request.method == 'POST':
        fullName = request.POST['fullname']
        user_email = request.POST['email']
        comment = request.POST['comment']

        comments = contactComment(fullName=fullName, user_email=user_email, comment=comment)
        comments.save()
        messages.info(request, 'Comment sent suceessfully...')
        return redirect('gallery')
