from unicodedata import category
from django.shortcuts import render, redirect
from .forms import AppointmentCreation, UserRegister, LoginForm, BlogCreation
from . models import Appointment, User, Blog
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages
from datetime import datetime, timedelta
import pickle
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


def home(request):
    return render(request, 'home.html')


def register_doc(request):
    if request.method == 'POST':
        form = UserRegister(request.POST, request.FILES)
        if form.is_valid():
            ref_id = form.cleaned_data['username']
            form.save()
            c = User.objects.get(Q(username=ref_id))
            print(c)
            c.is_doctor = True
            if(len(request.FILES) != 0):
                c.profile_pic = request.FILES['image']
            c.save()
            messages.success(
                request, 'You(Doctor) have registered successfully. Login In Now')
            return redirect('login')
        else:
            msg = 'Errors while validating the form. Try Again!'
            return render(request, 'register.html', {'form': form, 'msg': msg})
    else:
        form = UserRegister()
        return render(request, 'register.html', {'form': form})


def register_pat(request):
    if request.method == 'POST':
        form = UserRegister(request.POST, request.FILES)
        if form.is_valid():
            ref_id = form.cleaned_data['username']
            form.save()
            c = User.objects.get(Q(username=ref_id))
            print(c)
            c.is_patient = True
            if(len(request.FILES) != 0):
                c.profile_pic = request.FILES['image']
            c.save()
            messages.success(
                request, 'You(Patient) have registered successfully. Login In Now')
            return redirect('login')
        else:
            msg = 'Errors while validating the form. Try Again!'
            return render(request, 'registerpat.html', {'form': form, 'msg': msg})
    else:
        form = UserRegister()
        return render(request, 'registerpat.html', {'form': form})


def login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_doctor is True:
                data = Blog.objects.filter(is_draft=False)
                auth_login(request, user)
                return render(request, 'blogs.html', {'data': data})
            elif user is not None and user.is_doctor is False:
                data = Blog.objects.filter(is_draft=False)
                auth_login(request, user)
                return render(request, 'blogs.html', {'data': data})
            else:
                msg = 'You have entered incorrect username or password'
                return render(request, 'login.html', {'form': form, 'msg': msg})
        else:
            msg = 'Error has occured. Try Again'
    return render(request, 'login.html', {'form': form, 'msg': msg})


def blogs(request):
    data = Blog.objects.filter(is_draft=False)
    return render(request, 'blogs.html', {'data': data})


def drafts(request):
    data = Blog.objects.filter(is_draft=True, user=request.user)
    return render(request, 'drafts.html', {'data': data})


def myblogs(request):
    data = Blog.objects.filter(user=request.user, is_draft=False)
    return render(request, 'myblogs.html', {'data': data})


def createBlog(request):
    if request.method == 'POST':
        form = BlogCreation(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            user = request.user
            blog_category = form.cleaned_data['blog_category']
            summary = form.cleaned_data['summary']
            content = form.cleaned_data['content']
            is_draft = form.cleaned_data['is_draft']
            blog = Blog(
                user=user, title=title, blog_category=blog_category, summary=summary, content=content, is_draft=is_draft)
            blog.save()
            c = Blog.objects.get(Q(user=request.user) & Q(title=title))
            c.user = user
            if(len(request.FILES) != 0):
                c.blog_image = request.FILES['image']
            c.save()
            if(is_draft == False):
                messages.success(
                    request, 'Your Blog has been Successfully Created')
                return redirect('myblogs')
            else:
                messages.success(
                    request, 'Your Draft has been Successfully Created')
                return redirect('drafts')
        else:
            msg = 'Try Again!'
            return render(request, 'createblog.html', {'form': form, 'msg': msg})
    else:
        form = BlogCreation()
        return render(request, 'createblog.html', {'form': form})


def blogsall(request):
    data = Blog.objects.filter(is_draft=False)
    return render(request, 'blogs.html', {'data': data})


def mhealth(request):
    data = Blog.objects.filter(is_draft=False, blog_category='Mental Health')
    return render(request, 'blogs.html', {'data': data})


def heartdis(request):
    data = Blog.objects.filter(is_draft=False, blog_category='Heart Disease')
    return render(request, 'blogs.html', {'data': data})


def covid19(request):
    data = Blog.objects.filter(is_draft=False, blog_category='COVID19')
    return render(request, 'blogs.html', {'data': data})


def immun(request):
    data = Blog.objects.filter(is_draft=False, blog_category='Immunization')
    return render(request, 'blogs.html', {'data': data})


def appointment(request):
    data = User.objects.filter(is_doctor=True)
    print(data)
    return render(request, 'appointment.html', {'data': data})


def create_appoint(request, pk):
    doctor = User.objects.get(Q(pk=pk))
    first_name = doctor.first_name
    last_name = doctor.last_name
    full_name = str(first_name) + " " + str(last_name)
    if request.method == 'POST':
        form = AppointmentCreation(request.POST)
        if form.is_valid():
            app_date = form.cleaned_data['app_date']
            location = doctor.City
            user = request.user
            docof = User.objects.get(Q(username=doctor.username))
            app_time = form.cleaned_data['app_time']
            speciality = form.cleaned_data['speciality']
            end_time = calendar_app(full_name, app_date, app_time, location)
            print(type(end_time))
            appoint = Appointment(
                doctor_name=docof, patient_name=user, app_date=app_date, app_time=app_time, speciality=speciality, end_time=end_time)
            appoint.save()
            messages.success(
                request, 'Your Appointment has been scheduled')
            data = Appointment.objects.filter(patient_name=request.user)
            return render(request, 'viewappoints.html', {'data': data})
        else:
            msg = 'Errors while validating the form. Try Again!'
            return render(request, 'appointform.html', {'form': form, 'msg': msg})
    else:
        form = AppointmentCreation()
        return render(request, 'appointform.html', {'form': form, 'doctor': full_name})


def calendar_app(doctor, dateof, timeof, city):
    scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file(
        "app\client_secret.json", scopes=scopes)
    # credentials = flow.run_console()
    # pickle.dump(credentials, open("token.pkl", "wb"))

    credentials = pickle.load(open("token.pkl", "rb"))
    service = build("calendar", "v3", credentials=credentials)
    result = service.calendarList().list().execute()
    calendar_id = result['items'][1]['id']
    result = service.events().list(calendarId=calendar_id).execute()

    date_of = dateof.strftime("%d")
    month_of = dateof.strftime("%m")
    year_of = dateof.strftime("%Y")
    hour_of = timeof.strftime("%H")
    min_of = timeof.strftime("%M")
    sec_of = timeof.strftime("%S")

    start_time = datetime(int(year_of), int(month_of), int(
        date_of), int(hour_of), int(min_of), int(sec_of))
    end_time = start_time + timedelta(minutes=45)
    timezone = 'Asia/Kolkata'

    description = "Appointment with Doctor " + str(doctor)

    event = {
        'summary': 'Doctor Appointment',
        'location': str(city),
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24*60},
                {'method': 'popup', 'minutes': 15},
            ],
        },
    }

    service.events().insert(calendarId=calendar_id, body=event).execute()

    return end_time


def view_allapp(request):
    data = Appointment.objects.filter(patient_name=request.user)
    return render(request, 'viewappoints.html', {'data': data})
