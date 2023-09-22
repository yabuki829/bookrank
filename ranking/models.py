from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name
        
class Book(models.Model):
    title = models.CharField(max_length=255,unique=True)
    views = models.PositiveIntegerField(default=0)
    isbn = models.CharField(max_length=13,default="None")
    def __str__(self):
        return str(self.views) +" 件: " + self.title

class Data(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name="data")
    # moviemodelみたいなのを作成するのもあり？　-> メリットあんまりなさそうやからしない
    # サイトのタイトル
    title = models.CharField(max_length=255)
    # サイトのurl
    url = models.URLField()
    published_date = models.DateField()


    def __str__(self):
        return self.book.title + "「"+ self.title + "」"


class Check(models.Model):
  youtube_title = models.CharField(max_length=255)
  amazon_url = models.CharField(max_length=255)
  youtube_url = models.CharField(max_length=255)
  createdAt = models.DateTimeField(auto_now=True )

  def __str__(self):
        return self.youtube_title


# 1. 基本的にはyoutubeで紹介されている数でランキングをつける
