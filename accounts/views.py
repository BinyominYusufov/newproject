from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,logout,authenticate 
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator



def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if not username or not email or not password:
            return render(request, 'register.html', {
                'username': username,
                'email': email,
                'error': 'Заполни все поля!'
            })

        if password != confirm:
            return render(request, 'register.html', {
                'username': username,
                'email': email,
                'error': 'Пароли не совпадают!'
            })

        CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')



 
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'login.html', {
                'email': email,
                'error': 'Заполни все поля!'
            })

        user = authenticate(email=email, password=password)

        if user:
            if not user.email_verified:
                return render(request, 'login.html', {
                    'email': email,
                    'error': 'Подтверди email прежде чем войти!'
                })

            login(request, user)
            return redirect('/')

        return render(request, 'login.html', {
            'email': email,
            'error': 'Неверные данные!'
        })

        

def logout_view(request):
    try:
        logout(request)
        return redirect("login")
    except Exception as er:
        return HttpResponse(str(er))




User = get_user_model()
token_generator = PasswordResetTokenGenerator()

def confirm_email(request, user_id, token):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponse("User not found")

    if token_generator.check_token(user, token):
        user.email_verified = True
        user.save()
        return HttpResponse("Your email has been confirmed!")

    return HttpResponse("Invalid or expired confirmation link")
