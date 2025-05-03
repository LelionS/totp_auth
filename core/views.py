from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.http import HttpResponse

def totp_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        otp_token = request.POST.get('otp_token')

        user = authenticate(request, username=username, otp_token=otp_token)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, "Invalid username or code.")

    return render(request, 'core/login.html')


@login_required
def setup_totp_view(request):
    # Only create if user doesn't already have one
    device, created = TOTPDevice.objects.get_or_create(
        user=request.user,
        name="default",
        confirmed=True
    )
    config_url = device.config_url

    img = qrcode.make(config_url, image_factory=qrcode.image.svg.SvgImage)
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()

    return render(request, 'core/setup_totp.html', {'svg': svg})


@login_required
def home_view(request):
    return HttpResponse("Welcome! You are logged in.")
