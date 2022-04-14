from django.contrib.auth.models import AnonymousUser
from note.models import Note, Tag
from note.serializers import NoteSerializer, TagSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets

from note.permissions import IsOwner, IsPublicReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # Everyone can see tags
    permission_classes = (AllowAny,)


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            # This will protect editing public notes
            permission_classes = [IsPublicReadOnly]
        elif self.action == 'list':
            # This allows all to retrieve list, but query_set will handle to return proper one
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsOwner, IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            # Returns public notes for unauthenticated requests
            query_set = Note.objects.filter(public=True)
        else:
            # Filter objects for authorized user to get their own objects
            query_set = Note.objects.filter(owner=user)

        # Checking query params for tags filters
        tag_names = self.request.query_params.getlist('tags', [])
        if tag_names:
            # TODO: instead of hitting database to get tag_ids,
            #  change the custom slugrelatedfield in serializer to override get_value function
            tag_ids = Tag.objects.filter(name__in=tag_names)

            # distinct added to remove duplicate instance in filtering manyToMany fields
            query_set = query_set.filter(tags__in=tag_ids).distinct()

        return query_set
