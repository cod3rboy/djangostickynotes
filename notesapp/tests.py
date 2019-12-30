from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from . import models


class HomepageTest(TestCase):

    def test_url_path(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, template_name='notesapp/home.html')


class NewNotePageTest(TestCase):

    def setUp(self):
        self.temp_author = get_user_model().objects.create(
            username='user123',
            email='user123@email.com',
            password='password'
        )

        self.temp_note = models.Note()
        self.temp_note.title = "This is a title of note"
        self.temp_note.text = "This is the content of the note"
        self.temp_note.author = self.temp_author

    def test_url_path(self):
        response = self.client.get('/notes/new/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('note_new'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('note_new'))
        self.assertTemplateUsed(response, template_name='notesapp/notes_new.html')

    def test_new_note_added(self):
        response = self.client.post(reverse('note_new'), {
            'title': self.temp_note.title,
            'text': self.temp_note.text,
            'author': str(self.temp_note.author.id),
        })
        self.assertEqual(response.status_code, 302)
        last_note = models.Note.objects.all().order_by('-created_on')[0]
        self.assertEqual(self.temp_note.title, last_note.title)
        self.assertEqual(self.temp_note.text, last_note.text)
        self.assertEqual(self.temp_note.author, last_note.author)


class NoteDetailPageTest(TestCase):

    def setUp(self):
        self.temp_user = get_user_model().objects.create(
            username='tempuser123',
            email='tempuser@email.com',
            password='passtemp123',
        )
        self.temp_note = models.Note.objects.create(
            title="Temp note title",
            text="Temp note text is here",
            author=self.temp_user
        )

    def test_url_path(self):
        response = self.client.get('/notes/1/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('note_detail', args=[self.temp_note.pk]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('note_detail', args=[self.temp_note.pk]))
        self.assertTemplateUsed(response, 'notesapp/notes_detail.html')

    def test_page_content(self):
        response = self.client.get(reverse('note_detail', args=[self.temp_note.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.temp_note.title)
        self.assertContains(response, self.temp_note.text)
        self.assertContains(response, self.temp_note.author)


class NoteEditPageTest(TestCase):

    def setUp(self):
        temp_author = get_user_model().objects.create(
            username='tempuser123',
            email='tempuser@email.com',
            password='passtemp123',
        )
        self.temp_note = models.Note.objects.create(
            title='My note title',
            text='Text description of my node',
            author=temp_author,
        )

    def test_url_path(self):
        response = self.client.get('/notes/1/edit/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('note_edit', args=[self.temp_note.pk]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('note_edit', args=[self.temp_note.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='notesapp/notes_edit.html')

    def test_note_modified(self):
        new_title = 'This is modified title'
        new_text = 'This is modified note description'
        response = self.client.post(reverse('note_edit', args=[self.temp_note.pk]), {
            'title': new_title,
            'text': new_text,
        })
        self.assertEqual(response.status_code, 302)
        new_note = models.Note.objects.get(pk=self.temp_note.id)
        self.assertEqual(new_note.title, new_title)
        self.assertEqual(new_note.text, new_text)


class NoteDeletePageTest(TestCase):

    def setUp(self):
        temp_user = get_user_model().objects.create(
            username='tempuser123',
            email='tempuser123@email.com',
            password='passtemp123',
        )
        self.temp_note = models.Note.objects.create(
            title='Temp note title',
            text='This is description of temp note',
            author=temp_user
        )

    def test_url_path(self):
        response = self.client.get('/notes/1/delete/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('note_delete', args=[self.temp_note.pk]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('note_delete', args=[self.temp_note.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='notesapp/notes_delete.html')

    def test_note_deleted(self):
        response = self.client.post(reverse('note_delete', args=[self.temp_note.pk]))
        self.assertEqual(response.status_code, 302)
        note = None
        try:
            note = models.Note.objects.get(pk=self.temp_note.id)
        except models.Note.DoesNotExist:
            pass

        self.assertEqual(note, None)
