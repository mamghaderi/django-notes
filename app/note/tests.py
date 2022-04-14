import json
from http import HTTPStatus

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from rest_framework.test import force_authenticate
from rest_framework.test import APIClient

from note.views import NoteViewSet
from note.models import Note, Tag


class NoteViewSetTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()

    @staticmethod
    def create_note(user, number=1, public=False):
        notes = []

        for i in range(number):
            notes.append(Note.objects.create(title=f'title-{i}', owner=user, public=public))
        return notes

    @staticmethod
    def create_user(number=1):
        users = []
        for i in range(number):
            users.append(User.objects.create_superuser(
                username=f'test-user-{i}',
                password='somepass',
                email=f'some{i}@test.com'
            ))
        return users

    def test_list_note_viewset(self):

        user1, user2 = self.create_user(2)
        self.create_note(user1)
        self.create_note(user1, public=True)
        self.create_note(user2)

        url = '/note/views/Note'
        view_property = {'get': 'list'}

        # check anonymous user to just get public notes
        request = self.factory.get(url)
        response = NoteViewSet.as_view(view_property)(request)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['public'], True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # check user1 gets its own notes
        request = self.factory.get(url)
        force_authenticate(request, user=user1)
        response = NoteViewSet.as_view(view_property)(request)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['owner'], user1.pk)
        self.assertEqual(response.data['results'][1]['owner'], user1.pk)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # check user2 gets its own notes
        request = self.factory.get(url)
        force_authenticate(request, user=user2)
        response = NoteViewSet.as_view(view_property)(request)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['owner'], user2.pk)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_retrieve_note_viewset(self):

        user1, user2 = self.create_user(2)
        note1 = self.create_note(user1)[0]
        note2 = self.create_note(user1, public=True)[0]

        url = '/note/views/Note'
        view_property = {'get': 'retrieve'}

        # check anonymous user can not retrieve none public note
        request = self.factory.get(url)
        response = NoteViewSet.as_view(view_property)(request, pk=note1.id)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        # check anonymous user can retrieve public note
        request = self.factory.get(url)
        response = NoteViewSet.as_view(view_property)(request, pk=note2.id)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_filter_tag_in_note_viewset(self):

        user1, user2 = self.create_user(2)
        note1 = self.create_note(user1, public=True)[0]
        note2 = self.create_note(user1, public=True)[0]

        note1.tags.add(Tag.objects.get_or_create(name='tag1')[0])
        note1.tags.add(Tag.objects.get_or_create(name='tag2')[0])
        # note1.save()
        note2.tags.add(Tag.objects.get_or_create(name='tag2')[0])
        # note2.save()

        url = '/note/views/Note'
        view_property = {'get': 'list'}

        # check list with none existing tag
        request = self.factory.get(f'{url}?tags=nottag')
        response = NoteViewSet.as_view(view_property)(request)
        self.assertEqual(len(response.data['results']), 0)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # check list one note with tag1
        request = self.factory.get(f'{url}?tags=tag1')
        response = NoteViewSet.as_view(view_property)(request)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # check list two notes with tag2
        request = self.factory.get(f'{url}?tags=tag2')
        response = NoteViewSet.as_view(view_property)(request)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # check list all notes with tag2 or tag3
        request = self.factory.get(f'{url}?tags=tag1&tags=tag2')
        response = NoteViewSet.as_view(view_property)(request)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_note_viewset(self):
        data = json.dumps({
            "title": "title-sample",
            "body": "body1",
            "tags": ["tag1", "tags2"],
            "public": True
        })
        client = APIClient()
        user = self.create_user()[0]
        self.assertEqual(len(Tag.objects.all()), 0)
        client.force_authenticate(user=user)
        response = client.post('/notes/', data=data, content_type='application/json')
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(len(Tag.objects.all()), 2)
