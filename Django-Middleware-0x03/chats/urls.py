# from django.urls import path, include
# from rest_framework_nested import routers
# from .views import ConversationViewSet, MessageViewSet

# # Create main router
# router = routers.DefaultRouter()
# router.register(r'conversations', ConversationViewSet, basename='conversation')

# # Create nested router for messages under conversations
# conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
# conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# # URL patterns
# urlpatterns = [
#     path('', include(router.urls)),             # /conversations/
#     path('', include(conversations_router.urls)),  # /conversations/<pk>/messages/
# ]

from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = router.urls
