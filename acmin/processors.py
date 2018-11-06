from django.conf import settings

def extra_context(request):
    return {
        'app_name': getattr(settings, "APP_NAME"),
        "function_name": getattr(settings, "FUNCTION_NAME"),
    }
