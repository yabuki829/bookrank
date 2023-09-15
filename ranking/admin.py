from django.contrib import admin
from .models import Channel, Book, Check, Data

admin.site.register(Channel)

class BookAdmin(admin.ModelAdmin):
    ordering = ['-views']
    search_fields = ['title']


admin.site.register(Book,BookAdmin)
admin.site.register(Check)



class DataAdmin(admin.ModelAdmin):
    search_fields = ['title',"book__title"]
    raw_id_fields = ('book',)

admin.site.register(Data, DataAdmin)
# admin.site.register(Data)