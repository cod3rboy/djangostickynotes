import random
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from faker import Faker
from . import models


class HomepageTest(TestCase):

    def setUp(self):
        self.temp_user = get_user_model().objects.create_user(
            username='tempuser123',
            email='tempuser123@email.com',
            password='passtemp123',
        )
        login = self.client.login(username='tempuser123', password='passtemp123')
        self.assertTrue(login)
        self.fake = Faker()
        self.genders = [
            get_user_model().Gender.MALE,
            get_user_model().Gender.FEMALE,
            get_user_model().Gender.TRANSGENDER,
        ]

    def test_url_path(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, template_name='notesapp/home.html')

    def test_posts_appear(self):
        note_one = models.Note.objects.create(
            title='First Note',
            text='First Note Text',
            author=self.temp_user,
        )
        note_two = models.Note.objects.create(
            title='Second Note',
            text='Second Note Text',
            author=self.temp_user,
        )
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, note_one.get_short_title())
        self.assertContains(response, note_one.get_short_text())
        self.assertContains(response, note_two.get_short_title())
        self.assertContains(response, note_two.get_short_text())

    def test_posts_author(self):
        # Create more users and notes
        authors = []
        for i in range(0, 5):
            authors.append(
                get_user_model().objects.create_user(
                    first_name=self.fake.first_name(),
                    last_name=self.fake.last_name(),
                    email=self.fake.email(),
                    gender=str(random.choice(self.genders)),
                    username=get_random_string(length=15),
                    password=self.fake.password())
            )
        authors.append(self.temp_user)
        for i in range(0, 20):
            models.Note.objects.create(
                title=self.fake.sentence(),
                text=self.fake.text(max_nb_chars=100),
                author=random.choice(authors)
            )

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        notes = response.context['object_list']
        for note in notes:
            self.assertEqual(note.author.id, self.temp_user.id)

    def test_anonymous_user_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)


class NewNotePageTest(TestCase):

    def setUp(self):
        self.temp_user = get_user_model().objects.create_user(
            username='tempuser123',
            email='tempuser123@email.com',
            password='passtemp123',
        )
        login = self.client.login(username='tempuser123', password='passtemp123')
        self.assertTrue(login)

        self.temp_note = models.Note()
        self.temp_note.title = "This is a title of note"
        self.temp_note.text = "This is the content of the note"
        self.temp_note.author = self.temp_user

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

    def test_anonymous_user_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('note_new'))
        self.assertEqual(response.status_code, 302)


class NoteDetailPageTest(TestCase):

    def setUp(self):
        self.temp_user = get_user_model().objects.create_user(
            username='tempuser123',
            email='tempuser123@email.com',
            password='passtemp123',
        )
        login = self.client.login(username='tempuser123', password='passtemp123')
        self.assertTrue(login)

        self.fake = Faker()
        self.genders = [
            get_user_model().Gender.MALE,
            get_user_model().Gender.FEMALE,
            get_user_model().Gender.TRANSGENDER,
        ]

        self.temp_note = models.Note.objects.create(
            title=self.fake.sentence(),
            text=self.fake.text(max_nb_chars=100),
            author=self.temp_user
        )

    def test_url_path(self):
        response = self.client.get('/notes/' + self.temp_note.slug + '/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('note_detail', args=[self.temp_note.slug]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('note_detail', args=[self.temp_note.slug]))
        self.assertTemplateUsed(response, 'notesapp/notes_detail.html')

    def test_page_content(self):
        response = self.client.get(reverse('note_detail', args=[self.temp_note.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.temp_note.title)
        self.assertContains(response, self.temp_note.text)
        self.assertContains(response, self.temp_note.author)

    def test_restrict_to_view_note_of_other_user(self):
        password = self.fake.password()
        other_user = get_user_model().objects.create_user(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.fake.email(),
            gender=str(random.choice(self.genders)),
            username=get_random_string(15),
            password=password
        )
        other_note = models.Note.objects.create(
            title=self.fake.sentence(),
            text=self.fake.text(max_nb_chars=100),
            author=other_user,
        )
        response = self.client.get(reverse('note_detail', args=[other_note.slug]))
        self.assertEqual(response.status_code, 404)

    def test_context_has_domain_and_protocol(self):
        response = self.client.get(reverse('note_detail', args=[self.temp_note.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['domain'], None)
        self.assertNotEqual(response.context['protocol'], None)

    def test_anonymous_user_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('note_detail', args=[self.temp_note.slug]))
        self.assertEqual(response.status_code, 302)


class NoteEditPageTest(TestCase):

    def setUp(self):
        self.temp_user = get_user_model().objects.create_user(
            username='tempuser123',
            email='tempuser123@email.com',
            password='passtemp123',
        )
        login = self.client.login(username='tempuser123', password='passtemp123')
        self.assertTrue(login)
        self.fake = Faker()
        self.genders = [
            get_user_model().Gender.MALE,
            get_user_model().Gender.FEMALE,
            get_user_model().Gender.TRANSGENDER,
        ]
        self.temp_note = models.Note.objects.create(
            title=self.fake.sentence(),
            text=self.fake.text(max_nb_chars=100),
            author=self.temp_user,
        )

    def test_url_path(self):
        response = self.client.get('/notes/' + self.temp_note.slug + '/edit/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('note_edit', args=[self.temp_note.slug]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('note_edit', args=[self.temp_note.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='notesapp/notes_edit.html')

    def test_note_modified(self):
        new_title = 'This is modified title'
        new_text = 'This is modified note description'
        response = self.client.post(reverse('note_edit', args=[self.temp_note.slug]), {
            'title': new_title,
            'text': new_text,
        })
        self.assertEqual(response.status_code, 302)
        new_note = models.Note.objects.get(pk=self.temp_note.id)
        self.assertEqual(new_note.title, new_title)
        self.assertEqual(new_note.text, new_text)

    def test_restrict_to_edit_note_of_other_user(self):
        other_user = get_user_model().objects.create_user(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.fake.email(),
            gender=random.choice(self.genders),
            username=get_random_string(length=15),
            password=self.fake.password(),
        )
        other_note = models.Note.objects.create(
            title=self.fake.sentence(),
            text=self.fake.text(max_nb_chars=100),
            author=other_user,
        )
        # Restrict Get Method
        response = self.client.get(reverse('note_edit', args=[other_note.slug]))
        self.assertEqual(response.status_code, 404)
        # Restrict Post Method
        response = self.client.post(reverse('note_edit', args=[other_note.slug]), data={
            'title': self.fake.sentence(),
            'text': self.fake.text(max_nb_chars=100),
        })
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('note_edit', args=[self.temp_note.slug]))
        self.assertEqual(response.status_code, 302)


class NoteDeletePageTest(TestCase):

    def setUp(self):
        self.temp_user = get_user_model().objects.create_user(
            username='tempuser123',
            email='tempuser123@email.com',
            password='passtemp123',
        )
        login = self.client.login(username='tempuser123', password='passtemp123')
        self.assertTrue(login)
        self.fake = Faker()
        self.genders = [
            get_user_model().Gender.MALE,
            get_user_model().Gender.FEMALE,
            get_user_model().Gender.TRANSGENDER,
        ]
        self.temp_note = models.Note.objects.create(
            title=self.fake.sentence(),
            text=self.fake.text(max_nb_chars=100),
            author=self.temp_user
        )

    def test_url_path(self):
        response = self.client.get('/notes/' + self.temp_note.slug + '/delete/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('note_delete', args=[self.temp_note.slug]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('note_delete', args=[self.temp_note.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='notesapp/notes_delete.html')

    def test_note_deleted(self):
        response = self.client.post(reverse('note_delete', args=[self.temp_note.slug]))
        self.assertEqual(response.status_code, 302)
        note = None
        try:
            note = models.Note.objects.get(pk=self.temp_note.id)
        except models.Note.DoesNotExist:
            pass

        self.assertEqual(note, None)

    def test_restrict_to_delete_note_of_other_user(self):
        other_user = get_user_model().objects.create_user(
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            email=self.fake.email(),
            gender=random.choice(self.genders),
            username=get_random_string(length=15),
            password=self.fake.password(),
        )
        other_note = models.Note.objects.create(
            title=self.fake.sentence(),
            text=self.fake.text(max_nb_chars=100),
            author=other_user,
        )
        response = self.client.get(reverse('note_delete', args=[other_note.slug]))
        self.assertTrue(response.status_code, 404)
        response = self.client.post(reverse('note_delete', args=[other_note.slug]))
        self.assertTrue(response.status_code, 404)

    def test_anonymous_user_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('note_delete', args=[self.temp_note.slug]))
        self.assertEqual(response.status_code, 302)


class SharedNoteDetailPageView(TestCase):
    def setUp(self):
        self.temp_user_password = 'passtemp123'
        self.temp_user = get_user_model().objects.create_user(
            username='tempuser123',
            email='tempuser123@email.com',
            password=self.temp_user_password,
        )
        self.fake = Faker()
        self.genders = [
            get_user_model().Gender.MALE,
            get_user_model().Gender.FEMALE,
            get_user_model().Gender.TRANSGENDER,
        ]
        self.temp_note = models.Note.objects.create(
            title=self.fake.sentence(),
            text=self.fake.text(max_nb_chars=100),
            author=self.temp_user,
            shared=True,
        )

    def test_url_path(self):
        response = self.client.get('/notes/shared/' + self.temp_note.slug + '/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('shared_note_detail', args=[self.temp_note.slug]))
        self.assertTrue(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('shared_note_detail', args=[self.temp_note.slug]))
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'notesapp/shared_note_detail.html')

    def test_unshared_note_not_found(self):
        unshared_note = models.Note.objects.create(
            title=self.fake.sentence(),
            text=self.fake.text(max_nb_chars=100),
            author=self.temp_user,
            shared=False,
        )
        response = self.client.get(reverse('shared_note_detail', args=[unshared_note.slug]))
        self.assertEqual(response.status_code, 404)
