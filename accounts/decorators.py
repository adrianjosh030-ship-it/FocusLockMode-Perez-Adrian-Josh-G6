from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(*roles):
    """Allow only logged-in users whose role is in `roles`.

    Logged-out users go to the login page; users with the wrong role are sent
    back to their own dashboard.
    """

    def decorator(view):
        @wraps(view)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles:
                messages.error(request, "You do not have access to that page.")
                return redirect("accounts:dashboard")
            return view(request, *args, **kwargs)

        return wrapper

    return decorator
