import datetime
from uuid import uuid4

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Book,Author,BookInstance,Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView,UpdateView,DeleteView

from catalog.forms import RenewBookForm,CreateBookInstanceForm

from django.contrib.auth.decorators import login_required,permission_required


class BookInstanceUpdate(PermissionRequiredMixin,UpdateView):
    model = BookInstance
    fields = ['imprint','status','borrower','due_back']
    permission_required = 'catalog.can_mark_returned'
    template_name_suffix= '_update'
    def get_success_url(self):
        return reverse('bookinstances')

class BookInstanceDelete(PermissionRequiredMixin,DeleteView):
    model = BookInstance    
    permission_required = 'catalog.can_mark_returned'    
    def get_success_url(self):
        return reverse('bookinstances')

class AuthorCreate(CreateView):
    model=Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    initial = {'date_of_death':'11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(DeleteView):
    model=Author
    success_url = reverse_lazy('authors')

class BookInstanceList(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'


@login_required
@permission_required('catalog.can_mark_returned')
def create_bookinstance(request):    
  
    if request.method == 'POST':
        form = CreateBookInstanceForm(request.POST)
        if form.is_valid():
            
            cdata = form.cleaned_data
            newBookInstance = BookInstance(
                book=cdata['book'],
                imprint =cdata['imprint'],
                due_back = cdata['due_back'],
                borrower = cdata['borrower'],
                status = cdata['status'],
            )
            newBookInstance.save()
            next_url = 'bookinstances' if  request.POST.get('action') == 'Submit' else 'create_bookinstance'
            return HttpResponseRedirect(reverse(next_url))
    else:
        id = uuid4()
        form = CreateBookInstanceForm(initial={'id':id})
    context={
        'form':form,
    }
    return render(request,'catalog/bookinstance_form.html',context)

@login_required
@permission_required('catalog.can_mark_returned',raise_exception=True)
def renew_book_librarian(request,pk):
    book_instance = get_object_or_404(BookInstance,pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding)
        form = RenewBookForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # process the data in form.cleaned_data as required 
            # (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowed'))        
    
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={
            'renewal_date': proposed_renewal_date
        })
    context = {
        'form':form,
        'book_instance': book_instance
    }
    return render(request,'catalog/book_renew_librarian.html',context)

# Create your views here.
def index(request : HttpRequest):
    """View function for home page of site."""
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_genres':num_genres,
        'num_visits':num_visits,
    }
    return render(request, 'index.html',context=context)
    
class AuthorList(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetail(generic.DetailView):
    model = Author

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    
class BookDetailView(generic.DetailView):
    model = Book
    redirect_field_name = 'redirect_to'

class BookYearMonthListView(generic.ListView):
    model = Book
    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Book.objects.filter(release_date__year=year,release_date__month=month)        
    
def books_in_year(request, year, **kwargs):
    template_name = kwargs['my_template_name']
    book_list = Book.objects.filter(release_date__year=year)
    context = {
        'book_list' :book_list
    }
    return render(request,template_name,context= context)

class LoanedBooksByUserListView(LoginRequiredMixin ,generic.ListView):
    model = BookInstance
    paginate_by = 10
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    def get_queryset(self):
        return BookInstance.objects \
        .filter(borrower = self.request.user) \
        .filter(status__exact='o').order_by('due_back')

class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    permission_required = ('catalog.can_mark_returned')
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    def get_queryset(self):
        return BookInstance.objects \
            .filter(status__exact = 'o').order_by('due_back')
    