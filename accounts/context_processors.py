from django.conf import settings


def system_name(request):
    return {"SYSTEM_NAME": settings.SYSTEM_NAME}
