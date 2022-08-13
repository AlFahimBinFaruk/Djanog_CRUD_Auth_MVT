from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# login user
def loginUser(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)

        except:
            messages.error(request, 'User does not exist')

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Username OR password does not exit')

    return render(request, 'account/login.html')

# register user
def registerUser(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'account/register.html', {'form': form})


# logout user
def logoutUser(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')
