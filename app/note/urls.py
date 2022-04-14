from rest_framework import routers
from django.urls import path, include

from note.views import NoteViewSet, TagViewSet

router = routers.DefaultRouter()
router.register(r'notes', NoteViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
