from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from ranking.models import Book

class APIView(View):
    
    def get(self, request, *args, **kwargs):
        print("APIが呼び出されました")
        # books = Book.objects.order_by("-views").all()
        books = Book.objects.order_by("-views").prefetch_related('data').all()

        books_data = []
        for book in books:
            data_items = book.data.all() 
            
            data_list = [{
                "title": data.title,
                "url": data.url,
            } for data in data_items]

            book_info = {
                "title": book.title,
                # pointに変更する
                "views": book.views,
                "isbn": book.isbn,
                "data": data_list
            }

            books_data.append(book_info)
            response_data = {
                # books_countに変更する
                "total_books": len(books_data), 
                "books": books_data
            }

        return JsonResponse(response_data, safe=False)