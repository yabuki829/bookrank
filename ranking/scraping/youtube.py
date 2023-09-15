from apscheduler.schedulers.background import BackgroundScheduler
from googleapiclient.discovery import build
from time import sleep
from ..models import Channel, Book,Check,Data
from datetime import datetime
from .amazon import find_amazon_url,scrape_amazon_title
def scrape_videos():
		youtube = build('youtube', 'v3', developerKey='AIzaSyD7N6Ibv0QxqCejBvPNTqFT0JuwoLbHzig')
		
		for channel in Channel.objects.all():
				request = youtube.search().list(
						channelId=channel.youtube_id,
						maxResults=50
				)
				response = request.execute()

				for item in response['items']:
						video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
						video_title = item['snippet']['title']
						print(video_title)
						published_date = item['snippet']['publishedAt']

						description = item['snippet']['description']
						# amazon_url = find_amazon_url(description)
						# book_title = scrape_amazon_title(amazon_url)

						# Book.objects.create(
						#     book_title=book_title,
						#     youtube_title=video_title,
						#     youtube_url=video_url,
						#     published_date=published_date
						# )

def covertDate(date_string):
	date_format = "%Y/%m/%d"
# 文字列を日付オブジェクトに変換
	date_object = datetime.strptime(date_string, date_format)

	# 指定したフォーマットに変換して出力
	output_string = date_object.strftime( "%Y-%m-%dT%H:%M:%SZ")

	return output_string

def getChannelAllVideo(channnel_id):
		youtube = build('youtube', 'v3', developerKey="AIzaSyD7N6Ibv0QxqCejBvPNTqFT0JuwoLbHzig")
		channel_response = youtube.channels().list(
			part = 'contentDetails',
			id = channnel_id

		).execute()
		print("channel_response",channel_response)
		playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
		print("playlist_id",playlist_id)
		# playlist_idから全ての動画を取得する
		video_id_list = []
		# published_date = covertDate("2023/05/27")
		# print(published_date)
		request = youtube.playlistItems().list(
				part="snippet",
				maxResults=50,
				playlistId=playlist_id,
				fields="nextPageToken,items/snippet/resourceId/videoId",
				# publishedAfter=published_date
		)

		while request:
				response = request.execute()
				video_id_list.extend(list(map(lambda item: item["snippet"]["resourceId"]["videoId"], response["items"])))
				request = youtube.playlistItems().list_next(request, response)

		for i in range(len(video_id_list)):
			print("----",i+1,"本目の動画-----")
			getVideoFromYoutube(video_id_list[i])
		

def getVideoFromYoutube(youtube_video_ID):
		
	# descriptionにamazonのurlがあるかどうかを調べる
	# あればデータを保存する
	youtube = build('youtube', 'v3', developerKey="AIzaSyD7N6Ibv0QxqCejBvPNTqFT0JuwoLbHzig")
	videos_response = youtube.videos().list(
			part='snippet,statistics',
			
			id='{},'.format(youtube_video_ID)
	).execute()
	snippetInfo = videos_response["items"][0]["snippet"]
	# https://www.youtube.com/watch?v=-Rf1wE_mmNI ヒカキン
	video_url = "https://www.youtube.com/watch?v="+youtube_video_ID
	print("-----------------------------")

	published_at = snippetInfo['publishedAt'][:10]
	video_title = snippetInfo['title']
	
	channel_name = snippetInfo['channelTitle']
	channel_id = snippetInfo['channelId']

	# 動画の概要欄を取得する
	description = snippetInfo["description"]
	# 概要欄にamazonのurlを探す
	print(video_title) 
	urls = find_amazon_url(description)
	print(urls)
	if urls == None:
		return 

	
	data = Data.objects.filter(title=video_title,url=video_url)
	# 登録済みであれば飛ばす
	if len(data) != 0:
		print("登録済みです")
		return 

	for url in urls:
			sleep(10)
			book_title = scrape_amazon_title(url)
			if book_title == "NoSuchElementException":
				# タイトルが見つからない場合本でない場合が多い
				return	
			if book_title == None:
				# 目視でチェックする
				Check.objects.create(youtube_title=video_title,amazon_url=url,youtube_url=video_url)
				continue

			books = Book.objects.filter(title=book_title)
			# 本が登録されていなければ
			if len(books) == 0:
				book = Book.objects.create(title=book_title)
			else:
				book = books[0]
				
			Data.objects.create(
				book=book,
				title=video_title,
				url=video_url,
				published_date=published_at
			)
			print(book_title)


			
	



 



	


scheduler = BackgroundScheduler()
scheduler.add_job(scrape_videos, 'cron', hour=4)
scheduler.start()
