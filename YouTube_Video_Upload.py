from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
import os

# ----------------------logging in into the channel ---------------------------------#
channel = Channel()
#For the Credential file it is provide by the google cloud platform you can download from there
channel.login("client_secrets.json", "credentials.txt")


# ----------setting up the video that is going to be uploaded-------------------------#
def upload(path):
    all_files = os.listdir(path)
    for i in range(len(all_files)):
        video = LocalVideo(file_path=(os.path.join(path, all_files[i])))
        # --------------------setting snippet ---------------------------------#
        title = all_files[i][:-4]
        video.set_title(title)
        # video.set_description(
        #     f"This is the time lapse video captured by our IP Camera present at our construction site on {date} of our Toldot Yossef Project.\n תקציר ממה שקרה היום -  {yesterday}  , באתר הבניה של עמותת תולדות יוסף באופקים")
        video.set_tags(["Upload Test", "Content Creator", "Work Progression"])
        video.set_category(29)
        video.set_default_language("en-US")

        # # setting status
        video.set_embeddable(True)
        video.set_license("creativeCommon")


        video.set_privacy_status("public")
        video.set_public_stats_viewable(True)

        #---------------- setting thumbnail -------------------------------#
        thumbnail_path = "<THUMBNAIL FOLDER PATH>"
        list_image = os.listdir(thumbnail_path)
        if all_files[i].split('.')[0] == list_image[i].split('.')[0]:
            video.set_thumbnail_path(os.path.join(thumbnail_path, list_image[i])) 

        # ----------------------uploading video and printing the results-------------#
        video = channel.upload_video(video)
        print(video.id)
        full_video_link = f"https://www.youtube.com/watch?v={video.id}"
        print(f"fullvideo video link ---- {full_video_link}")
        print(video)

        # ------------------------------liking video---------------------------#
        video.like()
        return full_video_link
#----------------------folder location-----------------------------------#
path = "<FOLDER PATH>"
import time
for i in range(len(os.listdir(path))):
    print("Now We a uploading the video {i} in the give folder")
    upload(path)
    time.sleep(1800)