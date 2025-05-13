from django.shortcuts import render, redirect
import pyrebase
import datetime


firebase_config = {
    "apiKey": "AIzaSyCcc-FoMOcUS4mJfzaudrRfzhkBbITnn8w",
    "authDomain": "taskzilla-ad222.firebaseapp.com",
    "projectId": "taskzilla-ad222",
    "databaseURL": "https://taskzilla-ad222-default-rtdb.europe-west1.firebasedatabase.app",
    "storageBucket": "taskzilla-ad222.appspot.com",
    "messagingSenderId": "542053114688",
    "appId": "1:542053114688:web:834a8e6b24913268fbd0a5",
    "measurementId": "G-TQZ33L4FTG"
}
# Initialising database,auth and firebase for further use 
firebase=pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
database=firebase.database()

def home(request):
    return render(request,"Home.html")

def signIn(request):
    return render(request,"Login.html")

def postsignIn(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except Exception as e:
        message = "Неверный логин или пароль!"
        return render(request, "Login.html", {"message": message})
    
    # Проверяем, подтвержден ли email
    try:
        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        user_info = auth.get_account_info(session_id)
        email_verified = user_info['users'][0]['emailVerified']
        if not email_verified:
            del request.session['uid']  # Удаляем сессию, если email не подтвержден
            message = "Пожалуйста, подтвердите ваш email."
            return render(request, "Login.html", {
                "message": message,
                "email": email,
                "show_resend": True  # Показываем кнопку повторной отправки
            })
    except Exception as e:
        del request.session['uid']
        message = "Ошибка при проверке подтверждения email."
        return render(request, "Login.html", {"message": message})
    
    return render(request, "Home.html", {"email": email})

def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"Login.html")

def signUp(request):
    return render(request,"Registration.html")

def postsignUp(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    name = request.POST.get('name')
    
    try:
        # Создаем аккаунт в Firebase Authentication
        user = auth.create_user_with_email_and_password(email, password)
        uid = user['localId']  # Получаем UID нового пользователя

        # Подготавливаем данные для записи
        user_data = {
            "name": name,
            "email": email,
            "created_at": datetime.datetime.now().isoformat()
        }

        # Сохраняем данные в Realtime Database
        database.child("users").child(uid).set(user_data)

    except Exception as e:
        # Обрабатываем ошибки
        error_message = "Ошибка регистрации. "
        if "EMAIL_EXISTS" in str(e):
            error_message += "Пользователь c таким email уже существует."
        else:
            error_message += "Проверьте введенные данные."
        return render(request, "Registration.html", {"message": error_message})

    return render(request, "Login.html", {"message": "Регистрация успешна! Теперь выполните вход."})

def reset(request):
    return render(request, "Reset.html")

def postReset(request):
    email = request.POST.get('email')
    try:
        auth.send_password_reset_email(email)
        message  = "Письмо-восстановление пароля добавлено"
        return render(request, "Reset.html", {"msg":message})
    except:
        message  = "Что-то пошло не так, проверьте корректность данных."
        return render(request, "Reset.html", {"msg":message})
    
def resend_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # Аутентифицируемся для получения токена
            user = auth.sign_in_with_email_and_password(email, password)
            auth.send_email_verification(user['idToken'])
            message = "Письмо с подтверждением отправлено повторно. Проверьте вашу почту."
            return render(request, "Login.html", {"message": message})
        except:
            message = "Ошибка: Неверный email или пароль."
            return render(request, "Login.html", {
                "message": message,
                "email": email,
                "show_resend": True
            })
    return redirect('login')
    