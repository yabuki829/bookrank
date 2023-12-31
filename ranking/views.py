from django.shortcuts import render
from .models import Book,Channel,Data
from .methods import youtube,amazon

import time


def book_list(request):
    # youtube.getChannelAllVideo("UCrZ1UvZ5F1-2i1gll0hjjRg")
    # get_new_data()
    update_rank()
    # get_all_book_isbn()


    books = Book.objects.order_by("-views").all()[:10]

    return render(request, 'ranking/book_list.html',{'books': books})



# ランクを更新する
def update_rank():
    print("ランキングを更新")
    Book.objects.update(views=0)

    for book in Book.objects.all():
        num_data = Data.objects.filter(book=book)
        point = 0
        # 
        channels = []
        for data in num_data:
            data.channel
            if not data.channel in channels:
                point += 10
                channels.append(data.channel)
            else:
                point += 1

        book.views = point

        
        book.save()
    print("終了")


def get_all_book_isbn():
    books = Book.objects.order_by("-views").all()
    for i in range( len(books)):
        print(i+1,"位",books[i].title)
        if len(books[i].isbn) == 10 :
            continue
        
        if not amazon.check_asin(books[i].isbn): 
            
            isbn = amazon.scrape_isbn_for_amazon_A(books[i].title)

            print(isbn)
            if isbn != None:
                books[i].isbn = isbn
                books[i].save()
    print("終了")
        



def check_channel_on_data():
    youtube.get_channel_id_of_video("UCxnoA-FrO9AyDHM6ShgqRrg")
    # for channel in Channel.objects.all():
    #     print(channel.name)
        


# 毎日実行するやつ
def get_new_data():
    for channel in Channel.objects.all():
        print(channel.name)
        youtube.get_new_video(channel.youtube_id)

    pass

# 同じやつを削除する
def delete():
    objects = Data.objects.all()
    cnt = len(objects)

    delete_list = []

    for i in range(cnt-1):
        for j in range(i+1,cnt):
            if objects[i].title == objects[j].title and objects[i].book.title == objects[j].book.title:
                print("--------------------------")
                print(objects[i].title)
                print(objects[j].book.title)
                delete_list.append(objects[i])
    print(len(delete_list),"件")
    print(delete_list)

    for value in delete_list:
        value.delete()
    print("削除完了")
        
 
channels = [
    # 終了
    ["文学YouTuberベル", "UCL4QAojeGy6CJ9R2PwmlmJQ"],
    ["本解説のしもん塾", "UCIaQKvzS2QFoV9GWTXZ_YDQ"],
    ["アバタロー", "UCduDJ6s3mMchYMy2HvqalxQ"],
    ["OLめいの本要約チャンネル", "UCxnoA-FrO9AyDHM6ShgqRrg"],
    ["サラタメさん【サラリーマンYouTuber】", "UCaG7jufgiw4p5mphPPVbqhw"],# 188
    ["学識サロン", "UCC4NkFV-L-vVYD5z_Ei5dUA"],# 414
    ["中田敦彦のYouTube大学", "UCFo4kqllbcQ4nV83WCyraiw"],# 950
    ["サムの本解説ch", "UCcdd3kS52T9Zyo-SWfj86bA"], #461
     ["フェルミ漫画大学", "UC9V4eJBNx_hOieGG51NZ6nA"], # 611 【要約】「愛」するための哲学【白取春彦】 url壊れてる
    ["ほんタメ", "UC0zArNuGZKdvzSkfHbR9yLA"], # 984 古い動画は取得しないから実際はもっと少なそう
    ["本要約・書評の10分解説チャンネル", "UCp2xtXwztK9RvgmW8adtOZg"],# 85
    ["書評王に俺はなる", "UCgj5xk3r8cBIBLGMoF9LX7A"],# 188
     ["Kaho Miyake", "UCrZ1UvZ5F1-2i1gll0hjjRg"],# 21
    # まだ 

    

   
    

   
    

    ["梨ちゃんねる　文学系YouTuber", "UCwaQfJf70EbMhTfTc5kASYQ"],# 76
    

    ["ミステリー文学の本棚", "UCw9qkfAlPH1MuFEcFIXU-jQ"], # 369
    ["ビジョナリー大学", "UCLEnHp4Any3UNSOw_HT2BQg"],  # 64
    ["ちっこいピエロの本棚", "UCS9wlXLeVxTqXgPWU3kn7EQ"], # 164
    ["美女読書【ビジネス書の要約】", "UCqJm2FkNSBR0EuxR9mNYgBA"], #157
    ["文学系チャンネル【スケザネ図書館】", "UCLqjn__t2ORA0Yehvs1WzjA"],# 115

    ]


["東京の本屋さん　～街に本屋があるということ～", "UCC-Xr3O33ApZwx_V_pzVNVQ"], # 概要欄からのlink先にまとめられてる