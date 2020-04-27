from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required #TODO: Implement login req
import smtplib
from django.contrib.auth.models import User



def home(request):
    return render(request, 'home.html')


def signup(request):
    something_went_wrong = False
    if request.method == "POST":
        form_signup = RegisterForm(request.POST)
        if form_signup.is_valid():
            form_signup.save()
            return redirect('login')
        else:
            something_went_wrong = True
    else:
        form_signup = RegisterForm()

    return render(request, 'registration/signup.html', {'form_signup': form_signup,
                                                        'something_went_wrong': something_went_wrong})

def aboutme(request):
    return render(request, 'aboutme.html')

@login_required
def contact(request):
    something_went_wrong = False

    user = 'theinimicalwood@gmail.com'
    password = 'inimical121'
    mail_to = ["jarosinski91@gmail.com"]

    user_name = request.POST.get('username')
    user_mail = request.POST.get('usermail')
    account = request.user
    user_subject = request.POST.get('usersubject')
    mail_subject = 'Automatic e-mail from /contact/ from {}({}) - Subject: {}'.format(user_name, user_mail, user_subject)
    mail_body = request.POST.get('usertext')

    message = """From: {}
    Subject: {} 

    {}
    --------------------------------------
    sent by: {}
    e-mail: {}
    account: {}
    """.format(user_mail, mail_subject, mail_body, user_name, user_mail, account)

    if request.method == 'POST':
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(user, password)
            server.sendmail(user_mail, mail_to, message.encode('utf-8'))
            server.close()
        except:
            something_went_wrong = True
    return render(request, 'contact.html', {'something_went_wrong': something_went_wrong})

def game(request):
    return render(request, 'ingame/main_menu.html')
