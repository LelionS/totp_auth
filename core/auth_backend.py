from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice

User = get_user_model()

class TOTPOnlyBackend(BaseBackend):
    def authenticate(self, request, username=None, otp_token=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        devices = TOTPDevice.objects.filter(user=user, confirmed=True)
        for device in devices:
            if device.verify_token(otp_token):
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
