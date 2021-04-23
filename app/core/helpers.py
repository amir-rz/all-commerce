import pyotp
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def generate_key(model):
    """ User otp key generator """
    key = pyotp.random_base32()
    if is_unique(model, key):
        return key
    generate_key()


def generate_totp_for_instance(instance, digits=5, interval=600):
    return pyotp.TOTP(instance.base32_key, digits=digits, interval=interval)


def is_unique(model, key):
    try:
        model.objects.get(base32_key=key)
    except model.DoesNotExist:
        return True
    return False


class VerifyInstancePhoneNumber:
    """
    Verifies phone number of an instance e.g(User,Store,etc),
    by generating an OTP for it and sends it through sms,
    object must have this 3 fields:
    - base32_key
    - phone
    - phone_is_verified
    """

    def __init__(self, model, inc):
        if not inc.phone:
            raise ValueError("Object is invalid for verification.")
        self.inc = inc
        self.model = model

    def request_verification(self):
        """ generates a verification code for specific instance """
        self.inc.base32_key = generate_key(self.model)
        self.inc.phone_is_verified = False
        self.inc.save()
        totp = generate_totp_for_instance(self.inc)
        print(f"{self.inc.phone}: {totp.now()}")
        return totp

    def submit_verification(self, verification_code):
        """ generates a verification code for specific instance """
        totp = generate_totp_for_instance(self.inc)
        if totp.verify(verification_code):
            self.inc.phone_is_verified = True
            self.inc.base32_key = ""
            self.inc.save()
            return True
        return False
