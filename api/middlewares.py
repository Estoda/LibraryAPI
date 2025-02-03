from django.utils.deprecation import MiddlewareMixin


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """Extract JWT token from cookies and set it in the Authorization header."""
        access_token = request.COOKIES.get("access_token")  # Read token from cookies
        if access_token and "Authorization" not in request.headers:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"  # Set header
