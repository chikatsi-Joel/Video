from pytube import YouTube

def Download(url_video : str, url_save : str, file_name : str):
    youtubeObject = YouTube(url_video)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download(
            url_save,
            filename_prefix = file_name
        )
    except:
        print("An error has occurred")
    print("Download is completed successfully")

