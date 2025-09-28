from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# You can extend TokenObtainPairView if you want to customize claims
class MyTokenObtainPairView(TokenObtainPairView):
    pass

class MyTokenRefreshView(TokenRefreshView):
    pass
