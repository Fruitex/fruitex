from django.conf import settings
def debug_flags(request):
    return {
      'TEMPLATE_DEBUG': settings.TEMPLATE_DEBUG,
      'DEBUG': settings.DEBUG,
    }
