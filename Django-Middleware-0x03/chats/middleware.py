import logging
from datetime import datetime
from django.http import JsonResponse
import time
from collections import defaultdict
from django.http import JsonResponse

# Configure logger to write to requests.log
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    """
    Middleware to log each user's request with timestamp, user, and path.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response
 
class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to chat endpoints outside 6AM - 9PM.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only restrict messaging app URLs (adjust path if needed)
        if request.path.startswith('/api/'):  # assuming chat endpoints start with /api/
            current_hour = datetime.now().hour
            if current_hour < 6 or current_hour >= 21:
                return JsonResponse(
                    {'detail': 'Chat access is allowed only between 6AM and 9PM.'},
                    status=403
                )

        # Continue processing normally
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of messages sent by each IP.
    Example: 5 messages per minute.
    """
    # Class-level storage for requests per IP
    ip_message_log = defaultdict(list)  # { ip: [timestamps] }

    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = 5       # max messages
        self.window = 60     # time window in seconds

    def __call__(self, request):
        # Only track POST requests to message endpoints
        if request.method == "POST" and request.path.startswith("/api/messages/"):
            ip = self.get_client_ip(request)
            now = time.time()
            timestamps = self.ip_message_log[ip]

            # Remove timestamps older than the window
            self.ip_message_log[ip] = [ts for ts in timestamps if now - ts < self.window]

            if len(self.ip_message_log[ip]) >= self.limit:
                return JsonResponse(
                    {"detail": f"Message limit exceeded. Max {self.limit} messages per minute."},
                    status=429
                )

            # Log current request timestamp
            self.ip_message_log[ip].append(now)

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """Retrieve client IP address from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip


class RolePermissionMiddleware:
    """
    Middleware to enforce role-based permissions for chat endpoints.
    Only users with role 'admin' or 'moderator' can access protected actions.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only restrict certain paths (adjust as needed)
        protected_paths = [
            "/api/messages/delete/",
            "/api/messages/update/",
            "/api/conversations/delete/"
        ]

        if any(request.path.startswith(path) for path in protected_paths):
            user = getattr(request, "user", None)
            if not user or not user.is_authenticated:
                return JsonResponse({"detail": "Authentication required."}, status=401)

            # Check user role
            user_role = getattr(user, "role", None)  # assumes 'role' field exists on User
            if user_role not in ["admin", "moderator"]:
                return JsonResponse({"detail": "You do not have permission to perform this action."}, status=403)

        response = self.get_response(request)
        return response
