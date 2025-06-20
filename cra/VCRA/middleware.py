# accounts/middleware.py

from django.shortcuts import redirect

class BlockUserFromAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/adminover') and request.user.is_authenticated:
            if not request.user.is_staff and not request.user.is_superuser:
                return redirect('homelog')  # Adjust if needed
        return self.get_response(request)
