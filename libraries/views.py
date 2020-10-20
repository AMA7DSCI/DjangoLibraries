# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Library
from django.contrib.auth.models import User
from .forms import NewBookForm, NewLibraryForm
from .models import Library, Book
from django.contrib.auth.decorators import login_required



@login_required
def home(request):
    user = request.user
    libraries = Library.objects.filter(owner=user)
    return render(request, 'home.html', {'libraries': libraries})


@login_required
def library_books(request, pk):
    user = request.user
    library = get_object_or_404(Library, pk=pk, owner=user)
    allbooks = Book.objects.filter(library__pk=pk, library__owner=user)
    return render(request, 'books.html', {'library': library, 'allbooks': allbooks})




@login_required
def delete_library(request, pk):
    user = request.user    
    library = get_object_or_404(Library, pk=pk, owner=user)
    allbooks = Book.objects.filter(library__pk=pk, library__owner=user).delete()
    library.delete()
    return render(request, 'delete_library.html')


@login_required
def book_detail(request, pk, book_pk):
    user = request.user
    book = get_object_or_404(Book, library__pk=pk, pk=book_pk, library__owner=user)
    return render(request, 'book_detail.html', {'book': book})


@login_required
def new_library(request):
    user = request.user
    if request.method == 'POST':
        form = NewLibraryForm(request.POST)         
        if form.is_valid():
            library = form.save(commit=False)
            library.owner = user
            library = Library.objects.create(
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'), 
                location = form.cleaned_data.get('location'),
                owner=user
                )
            return redirect('home')
    else:
        form = NewLibraryForm()
    return render(request, 'new_library.html', {'form': form})


@login_required
def new_book(request, pk):
    user = request.user    
    library = get_object_or_404(Library, pk=pk, owner=user)
    if request.method == 'POST':
        form = NewBookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.library = library
            book = Book.objects.create(
                name=form.cleaned_data.get('name'),
                authors=form.cleaned_data.get('authors'),
                notes=form.cleaned_data.get('notes'), 
                library=library
            )
            return redirect('library_books', pk=library.pk)
    else:
        form = NewBookForm()
    return render(request, 'new_book.html', {'library': library, 'form': form})


@login_required
def edit_book(request, pk, book_pk):
    user = request.user    
    library = get_object_or_404(Library, pk=pk, owner=user)
    book = get_object_or_404(Book, library__pk=pk, pk=book_pk, library__owner=user)
    form = NewBookForm(request.POST or None, instance=book)
    if request.method == 'POST':
        form = form
        if form.is_valid():
            book = form.save(commit=False)
            book.library = library
            book.name=form.cleaned_data.get('name')
            book.authors=form.cleaned_data.get('authors')
            book.notes=form.cleaned_data.get('notes') 
            book.save()
            return redirect('library_books', pk=library.pk)
    else:
        form = form
    return render(request, 'edit_book.html', {'library': library, 'form': form, 'book': book})


@login_required
def delete_book(request, pk, book_pk):
    user = request.user    
    library = get_object_or_404(Library, pk=pk, owner=user)
    book = get_object_or_404(Book, library__pk=pk, pk=book_pk, library__owner=user)
    book.delete()
    return render(request, 'delete_book.html', {'library': library})

