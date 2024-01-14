from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackEnd(ModelBackend):
    def authenticate(self, request=None, email=None, phone_number=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            if email:
                user = UserModel.objects.get(email=email)
            elif phone_number:
                user = UserModel.objects.get(phone_number=phone_number)
            else:
                return None
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
