from django.test import TestCase
from django.urls import resolve, reverse
from ..models import Library, Book
from ..views import home, library_books, new_book
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# Create your tests here.


class HomeTests(TestCase):
    def setUp(self):
        username = 'john'
        password = '123'
        user = User.objects.create_user(username=username, email='john@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.library = Library.objects.create(name='TrialLibrary', description='Library Trial', owner=user)
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        library_books_url = reverse('library_books', kwargs={'pk': self.library.pk})
        self.assertContains(self.response, 'href="{0}"'.format(library_books_url))


class LibraryBooksTests(TestCase):
    def setUp(self):
        username = 'john'
        password = '123'
        user = User.objects.create_user(username=username, email='john@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.library = Library.objects.create(name='TrialLibrary', description='Library Trial', owner=user)
        url = reverse('home')
        self.response = self.client.get(url)
        #Library.objects.create(name='LibraryBooksTrial', description='Trial Library for Tests') - try this as alternative construction
        # does not work - perhaps for all other similar tests too

    def test_libary_books_view_success_status_code(self):
        url = reverse('library_books', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_library_books_view_not_found_status_code(self):
        url = reverse('library_books', kwargs={'pk': 9})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_library_books_url_resolves_library_books_view(self):
        view = resolve('/library/1/')
        self.assertEquals(view.func, library_books)

    def test_library_books_view_contains_navigation_links(self):
        library_books_url = reverse('library_books', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_book_url = reverse('new_book', kwargs={'pk':1})

        response = self.client.get(library_books_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_book_url))


class NewBookTests(TestCase):
    def setUp(self):
        username = 'john'
        password = '123'
        user = User.objects.create_user(username=username, email='john@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.library = Library.objects.create(name='TrialLibrary', description='Library Trial', owner=user)
        url = reverse('home')
        self.response = self.client.get(url)
 
 
    def test_new_book_view_success_status_code(self):
        url = reverse('new_book', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_book_view_not_found_status_code(self):
        url = reverse('new_book', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_book_url_resolves_new_book_view(self):
        view = resolve('/library/1/new/')
        self.assertEquals(view.func, new_book)

    def test_new_book_view_contains_link_back_to_board_topics_view(self):
        new_book_url = reverse('new_book', kwargs={'pk': 1})
        library_books_url = reverse('library_books', kwargs={'pk': 1})
        response = self.client.get(new_book_url)
        self.assertContains(response, 'href="{0}"'.format(library_books_url))

    def test_csrf(self):
        url = reverse('new_book', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_book_valid_data(self):
        url = reverse('new_book', kwargs={'pk': 1})
        data = {
            'name': 'Test title',
            'authors': 'Test authors'
        }
        response = self.client.post(url, data)
        self.assertTrue(Book.objects.exists())

    def test_new_book_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_book', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_book_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_book', kwargs={'pk': 1})
        data = {
            'name': '',
            'authors': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Book.objects.exists())