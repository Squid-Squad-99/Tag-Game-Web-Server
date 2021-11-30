from django.shortcuts import render, redirect
from .forms import MyUserCreationForm
# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup-success')
    else:
        form = MyUserCreationForm()
    return render(request, "signup.html", {'form': form})


def signup_success(request):
    return render(request, "signup_success.html")