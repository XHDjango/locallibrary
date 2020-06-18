# -*- coding:utf-8 -*-
'''
@Description: 目录应用程序URL包含在项目中，并映射 catalog／，因此访问此映射程序的URL必须从 catalog／开始（在正斜杠之后，映射程序正在工作于所有URL字符串）
@Author: lamborghini1993
@Date: 2019-03-07 20:19:42
@UpdateDate: 2019-03-11 17:20:24
'''

from django.urls import path, include
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),

    # 对于书本详细信息路径，URL 模式使用特殊语法，来捕获我们想要查看的书本的特定 id。
    # 语法非常简单：尖括号定义要捕获的URL部分，包含视图可用于访问捕获数据的变量的名称。
    # 例如，<something> 将捕获标记的模式，并将值作为变量 “something” ，传递给视图。
    # 您可以选择在变量名称前，加上一个定义数据类型的转换器规范（int，str，slug，uuid，path）。
    #
    # 在这里，我们使用 '<int:pk>' 来捕获 book id，它必须是一个整数，并将其作为名为 pk 的参数（主键的缩写）传递给视图。
    # 所有pk的意思是主键，不可改为其他字段
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),

    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),

    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),

]
