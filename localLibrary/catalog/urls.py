from xml.etree.ElementInclude import include
from django.urls import path,re_path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('books/',views.BookListView.as_view(),name='books'),
    path('authors/',views.AuthorList.as_view(),name='authors'),
    re_path(r'^books/year=(?P<year>[0-9]{4})$',views.books_in_year,{'my_template_name':'catalog/book_list.html'},name='books_in_year'),
    re_path(r'^books/year=(?P<year>[0-9]{4})/month=(?P<month>[0-9]{2})$',views.BookYearMonthListView.as_view(),name='books_in_year_month'),
    path('books/<int:pk>',views.BookDetailView.as_view(),name='book_detail'),
    path('authors/<int:pk>',views.AuthorDetail.as_view(),name='author_detail'),
    path('mybooks/',views.LoanedBooksByUserListView.as_view(),name='my_borrowed'),
    path('borrowed/',views.LoanedBooksListView.as_view(),name='borrowed'),
    path('author/create/',views.AuthorCreate.as_view(),name='author_create'),
    path('author/<int:pk>/update',views.AuthorUpdate.as_view(),name='author_update'),
    path('author/<int:pk>/delete',views.AuthorDelete.as_view(),name='author_delete'),
    
    path('bookinstances',views.BookInstanceList.as_view(),name='bookinstances'),
    path('bookinstance/create/',views.create_bookinstance,name='create_bookinstance'),
    path('bookinstance/<uuid:pk>/update',views.BookInstanceUpdate.as_view(),name='bookinstance_update'),
    path('bookinstance/<uuid:pk>/delete',views.BookInstanceDelete.as_view(),name='bookinstance_delete'),


]

urlpatterns +=[
    path('book/<uuid:pk>/renew/',views.renew_book_librarian,name='renew_book_librarian')
]
