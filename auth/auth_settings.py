from django.conf import settings

class Settings(object):
    def __init__(self, **kwargs):
        self.defaults = kwargs

    def __getattr__(self, key):
        return getattr(settings, 'USERPROFILES_%s' % key, self.defaults[key])

ACCOUNT_SETTING = Settings(
    ACCOUNT_ACTIVATION_DAYS = 30,
    ALLOW_TO_CHANGE_EMAIL = True,
    NEED_ACTIVATION = True,
)
