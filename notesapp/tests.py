from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from . import models


class HomepageTest(TestCase):

    def test_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, template_name='notesapp/home.html')


class NewNotePageTest(TestCase):
    temp_note = None
    temp_author = None

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

    def test_status_code(self):
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
    temp_note = None
    temp_user = None

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

    def test_status_code(self):
        response = self.client.get('/notes/1/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('note_detail', args=[self.temp_note.pk]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('note_detail', args=[self.temp_note.pk]))
        self.assertTemplateUsed(response, 'notesapp/notes_detail.html')

    def test_page_content(self):
        response = self.client.get(reverse('note_detail',  args=[self.temp_note.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.temp_note.title)
        self.assertContains(response, self.temp_note.text)
        self.assertContains(response, self.temp_note.author)
