from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from functools import wraps
from .EmailBackend import EmailBackend
from django.http import HttpResponse


def require_fee_payment(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user

        if user.is_authenticated and user.user_type == '3':
            if not user.has_paid_fees() and user.payment_required:
                user.payment_required = False
                user.save()

                logout(request)  # Using 'logout' from 'django.contrib.auth'

                return redirect(reverse_lazy('payment_required'))

        if user.is_authenticated and not user.has_paid_fees():
            logout(request)  # Using 'logout' from 'django.contrib.auth'

            return redirect(reverse_lazy('payment_required'))

        return view_func(request, *args, **kwargs)

    return wrapper


def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home"))
        elif request.user.user_type == '2':
            return redirect(reverse("staff_home"))
        elif request.user.user_type == '3':
            if request.user.has_paid_fees():
                return redirect(reverse("student_home"))
            else:
                return redirect(reverse("payment_required"))
    return render(request, 'main_app/login.html')


@require_fee_payment
def doLogin(request, **kwargs):
    if request.method != 'POST':
        return HttpResponse("<h4>Denied</h4>")
    else:
        user = EmailBackend.authenticate(
            request,
            username=request.POST.get('email'),
            password=request.POST.get('password')
        )
        if user is not None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("admin_home"))
            elif user.user_type == '2':
                return redirect(reverse("staff_home"))
            elif user.user_type == '3':
                if user.has_paid_fees():
                    return redirect(reverse("student_home"))
                else:
                    return redirect(reverse("payment_required"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")


def payment_required(request):
    return HttpResponse("Profile has been locked,+\
                         Kindly connect with tech team.")


def logout_user(request):
    if request.user is not None:
        logout(request)
    return redirect("/")

from django.shortcuts import render, redirect
from .forms import EventForm
from .models import Event

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            create_google_calendar_event(event)
            return redirect('create_event')
    else:
        form = EventForm()
    return render(request, 'hod_template/schedule_meeting.html', {'form': form})


import pytz
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Your existing code
service_account_email = "sk-academy@neat-fin-392006.iam.gserviceaccount.com"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

credentials = service_account.Credentials.from_service_account_file('neat.json')
scoped_credentials = credentials.with_scopes(SCOPES)


def build_service():
    service = build("calendar", "v3", credentials=scoped_credentials)
    return service


def create_google_calendar_event(event):
    service = build_service()

    start_datetime = event.start_datetime.astimezone(pytz.utc)
    end_datetime = event.end_datetime.astimezone(pytz.utc)
    event = (
        service.events()
        .insert(
            calendarId="primary",
            body={
                "summary": event.title,
                "description": "Bar",
                "start": {"dateTime": start_datetime.isoformat()},
                "end": {"dateTime": end_datetime.isoformat()},
            },
        )
        .execute()
    )

    print(event)
