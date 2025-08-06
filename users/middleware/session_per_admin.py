# users/middleware/session_per_admin.py

class AdminPanelSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Use separate session cookies for each admin panel
        if request.path.startswith('/limited-admin/'):
            request.session_cookie_name = 'limited_admin_sessionid'
        else:
            request.session_cookie_name = 'main_admin_sessionid'

        response = self.get_response(request)

        # Make sure correct cookie is set
        if hasattr(request, 'session_cookie_name') and request.session.session_key:
            response.set_cookie(
                request.session_cookie_name,
                request.session.session_key,
                httponly=True,
                samesite='Lax',
                secure=False,
            )

        return response
