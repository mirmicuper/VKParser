#link - https://www.tiktok.com/@kucher135
from TikTokApi import TikTokApi
import os
api = TikTokApi()
results = 10
directory = "trending"
# Creates the new directory
if not os.path.isdir(directory):
  os.mkdir(directory)
trending = api.trending(count=results)
for tiktok in trending:
  video_data = api.get_Video_By_TikTok(tiktok)
  save_file = "downloads/{}.mp4".format(tiktok['id'])
  with open(save_file, 'wb') as tiktok_output:
    tiktok_output.write(video_data)
    