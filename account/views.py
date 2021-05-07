from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls.base import reverse
from .forms import UserRegistrationForm, LoginForm
from .models import CustomUserModel

# Create your views here.


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_field = None
            try:
                user_field = CustomUserModel.objects.get(username=cd["username"])
            except CustomUserModel.DoesNotExist:
                try:
                    user_field = CustomUserModel.objects.get(email=cd["username"])
                except CustomUserModel.DoesNotExist:
                    pass
            if user_field:
                user = authenticate(
                    request, username=user_field.email, password=cd["password"]
                )
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(reverse("blog:published_posts"))
                    else:
                        return HttpResponse("Disabled account")
                else:
                    print(request.session)
                    messages.error(request, f"Incorrect password")
                    return render(request, "account/login.html", {"form": form})
            else:
                messages.error(
                    request, "Please check your username and or Email is correct"
                )
                return render(request, "account/login.html", {"form": form})
    else:
        form = LoginForm()
        return render(request, "account/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            context = {"new_user": new_user}
            return render(request, "account/register_done.html", context)
    else:
        user_form = UserRegistrationForm()
    context = {"user_form": user_form}
    return render(request, "account/register.html", context)
