import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, sub, timestamp):
        return (six.text_type(sub.pk) + six.text_type(timestamp))

emailVerificationToken = TokenGenerator()
