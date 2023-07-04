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
