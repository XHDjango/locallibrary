# -*- coding:utf-8 -*-
'''
@Description: 注册模型
@Author: lamborghini1993
@Date: 2019-03-07 20:03:04
@UpdateDate: 2019-03-11 17:14:05
'''
from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# admin.site.register(Genre)
# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)


# 和上面方法一样功能
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


class BookInstanceInline(admin.TabularInline):
    model = BookInstance


class AuthorInline(admin.TabularInline):
    model = Author


class BookInline(admin.TabularInline):
    model = Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    # 关联记录的内联编辑
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # 列表过滤器，右侧显示
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    # 使用 fieldsets 属性添加“部分”以在详细信息表单中对相关的模型信息进行分组。
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


class AuthorAdmin(admin.ModelAdmin):
    # 配置列表视图
    list_display = ('name', 'date_of_birth', 'date_of_death')
    # 控制哪些字段布局，'date_of_birth', 'date_of_death'在同一行
    fields = ['name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]


admin.site.register(Author, AuthorAdmin)
