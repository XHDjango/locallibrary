# -*- coding:utf-8 -*-
'''
@Description: 视图是处理HTTP请求的功能，根据需要从数据库获取数据，
    通过使用HTML模板呈现此数据生成HTML页面，然后以HTTP响应返回HTML以显示给用户。
    索引视图遵循此模型 - 它提取有关数据库中有多少Book，
    BookInstance 可用 BookInstance 和 Author 记录的信息，
    并将其传递给模板以进行显示。
@Author: lamborghini1993
@Date: 2019-03-07 20:03:04
@UpdateDate: 2019-03-11 17:36:51
'''

from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin   # 只有登录用户才能调用此视图


def index(request):
    """
    View function for home page of site.
    """
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()    # The 'all()' is implied by default.

    sVisits = "num_visits"
    num_visits = request.session.get(sVisits, 0)
    request.session[sVisits] = num_visits + 1

    return render(
        request,
        'index.html',
        context={
            "num_books": num_books,
            "num_instances": num_instances,
            "num_instances_available": num_instances_available,
            "num_authors": num_authors,
            sVisits: num_visits,
        }
    )


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5]  # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

    # def get_queryset(self):
    #     """
    #     覆盖get_queryset()方法，来更改返回的记录列表。这比仅仅设置queryset属性更灵活
    #     """
    #     # return Book.objects
    #     return Book.objects.filter(title__icontains='三')[:5]

    def get_context_data(self, **kwargs):
        """
        覆盖get_context_data() ，以将其他上下文变量传递给模板（例如，默认情况下传递书本列表）。下面的片段，显示了如何将一个名为“some_data”的变量添加到上下文中（然后它将作为一个模板变量，而被提供）
        """
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    # template_name 默认是 name_mode.html(author_detail.html)
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
