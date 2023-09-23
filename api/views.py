from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from ranking.models import Book

class APIView(View):
    
    def get(self, request, *args, **kwargs):
        books = Book.objects.order_by("-views").all()[:20]

        books_data = []
        for book in books:
            data_items = book.data.all() 
            data_list = [{
                "title": data.title,
                "url": data.url,
            } for data in data_items]

            book_info = {
                "title": book.title,
                "views": book.views,
                "isbn": book.isbn,
                "data": data_list
            }
            books_data.append(book_info)

        return JsonResponse(books_data, safe=False)