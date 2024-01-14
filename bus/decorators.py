# decorators.py

from functools import wraps
from django.shortcuts import redirect


def user_type_required(user_types=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user's user_type is in the allowed user_types
            if request.user.user_type in user_types:
                return view_func(request, *args, **kwargs)
            else:
                # Redirect or deny access, you can customize this part
                # Redirect to the index page or another suitable page
                return redirect('index')

        return _wrapped_view

    return decorator
