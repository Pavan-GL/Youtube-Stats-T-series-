#from youtube_statistics import YTstats
from yt import YTstats


API_KEY="AIzaSyCR7B_7-Wyi5wp0TK1vLMQw71sAINSUjH8"
channel_id="UCq-Fj5jknLsUf-MWSy4_brA"

yt=YTstats(API_KEY,channel_id)
yt.get_channel_statistics()
yt.get_channel_video_data()
yt.dump()