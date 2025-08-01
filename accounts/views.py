import logging
import requests
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

logger = logging.getLogger(__name__)

class RegisterView(View):
    model = CustomUser
    template_name = 'accounts/html/register.html'
    success_url = reverse_lazy('home:home')

    def get(self, request, *args, **kwargs):
        context = {
            'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY,
            'first_name': '',
            'last_name': '',
            'email': '',
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # دریافت مقادیر با پیش‌فرض خالی
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        honeypot = request.POST.get('honeypot', '')
        recaptcha_response = request.POST.get('g-recaptcha-response', '')

        # بررسی Honeypot
        if honeypot:
            logger.warning(f"Honeypot triggered for email: {email}")
            messages.error(request, 'ربات تشخیص داده شد!')
            return self.form_invalid(first_name, last_name, email)

        # اعتبارسنجی reCAPTCHA v2
        if not recaptcha_response:
            logger.warning(f"reCAPTCHA missing for email: {email}")
            messages.error(request, 'لطفاً کپچا را تأیید کنید.')
            return self.form_invalid(first_name, last_name, email)

        # درخواست به API Google برای اعتبارسنجی
        recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response,
            'remoteip': request.META.get('REMOTE_ADDR', '')
        }
        response = requests.post(recaptcha_url, data=payload)
        result = response.json()

        if not result.get('success'):
            logger.warning(f"reCAPTCHA failed for email: {email}, errors: {result.get('error-codes', [])}")
            messages.error(request, 'خطای کپچا: لطفاً دوباره تلاش کنید.')
            return self.form_invalid(first_name, last_name, email)

        # اعتبارسنجی داده‌ها
        if not all([first_name, last_name, email, password1, password2]):
            messages.error(request, 'لطفاً تمام فیلدها را پر کنید.')
            return self.form_invalid(first_name, last_name, email)

        if password1 != password2:
            messages.error(request, 'رمزهای عبور مطابقت ندارند.')
            return self.form_invalid(first_name, last_name, email)

        if len(password1) < 8:
            messages.error(request, 'رمز عبور باید حداقل ۸ کاراکتر باشد.')
            return self.form_invalid(first_name, last_name, email)

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'این ایمیل قبلاً ثبت شده است.')
            return self.form_invalid(first_name, last_name, email)

        # ایجاد کاربر
        try:
            user = CustomUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password1,
                is_active=True,
            )
            user.save()
            return redirect(self.success_url)
        except Exception as e:
            logger.error(f"Registration error for email: {email}, error: {str(e)}")
            messages.error(request, f'خطا در ثبت‌نام: {str(e)}')
            return self.form_invalid(first_name, last_name, email)

    def form_invalid(self, first_name, last_name, email):
        context = {
            'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY,
            'first_name': first_name or '',
            'last_name': last_name or '',
            'email': email or '',
        }
        return render(self.request, self.template_name, context)
    




class LoginView(View):
    template_name = 'accounts/html/login.html'
    success_url = reverse_lazy('home:home')

    def get(self, request, *args, **kwargs):
        context = {
            'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY,
            'email': '',
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        honeypot = request.POST.get('honeypot', '')
        recaptcha_response = request.POST.get('g-recaptcha-response', '')

        # بررسی Honeypot
        if honeypot:
            logger.warning(f"Honeypot triggered for email: {email}")
            messages.error(request, 'ربات تشخیص داده شد!')
            return self.form_invalid(email)

        # اعتبارسنجی reCAPTCHA v2
        if not recaptcha_response:
            logger.warning(f"reCAPTCHA missing for email: {email}")
            messages.error(request, 'لطفاً کپچا را تأیید کنید.')
            return self.form_invalid(email)

        # درخواست به API Google
        recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response,
            'remoteip': request.META.get('REMOTE_ADDR', '')
        }
        response = requests.post(recaptcha_url, data=payload)
        result = response.json()

        if not result.get('success'):
            logger.warning(f"reCAPTCHA failed for email: {email}, errors: {result.get('error-codes', [])}")
            messages.error(request, 'خطای کپچا: لطفاً دوباره تلاش کنید.')
            return self.form_invalid(email)

        # اعتبارسنجی داده‌ها
        if not all([email, password]):
            messages.error(request, 'لطفاً تمام فیلدها را پر کنید.')
            return self.form_invalid(email)

        # احراز هویت کاربر
        user = authenticate(request, username=email, password=password)
        if user is None:
            logger.warning(f"Authentication failed for email: {email}")
            messages.error(request, 'ایمیل یا رمز عبور اشتباه است.')
            return self.form_invalid(email)

        # ورود کاربر
        try:
            login(request, user)
            messages.success(request, 'ورود با موفقیت انجام شد!')
            return redirect(self.success_url)
        except Exception as e:
            logger.error(f"Login error for email: {email}, error: {str(e)}")
            messages.error(request, f'خطا در ورود: {str(e)}')
            return self.form_invalid(email)

    def form_invalid(self, email):
        context = {
            'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY,
            'email': email or '',
        }
        return render(self.request, self.template_name, context)
    



class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return redirect(reverse_lazy('home:home'))