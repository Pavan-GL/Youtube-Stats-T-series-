import requests
import json

class YTstats:
    
    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data=None
    
    
    def get_channel_statistics(self):
        """Extract the channel statistics"""
        print('get channel statistics...')
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
       # print(url)
        json_url=requests.get(url)
        data=json.loads(json_url.text)
        #print(data)
        
        try:
            data=data["items"][0]["statistics"]
        except:
            data=None
        self.channel_statistics=data
        return data
    
    
    def get_channel_video_data(self):
        channel_videos=self._get_channel_videos(limit=50)
        print(len(channel_videos))
        
        
        
    def _get_channel_videos(self,limit=None):
        url=f'https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date'
        if limit is not None and isinstance(limit,int):
            url += "&maxResults=" + str(limit)
       # print(url)
        
        vid,npt =self._get_channel_videos_per_page(url)
       # idx=0
        while(npt is not None):
            nexturl = url + "&pageToken=" + npt
            next_vid,npt=self._get_channel_videos_per_page(nexturl)
            vid.update(next_vid)
           # idx+=1
        return vid
            
        
    def _get_channel_videos_per_page(self,url):
        json_url=requests.get(url)
        data=json.loads(json_url.text)
        channel_videos=dict()
        if 'items' not in data:
            return channel_videos, None
        #nextPageToken = data.get("nextPageToken", None)
        
        item_data=data['items']
        nextPageToken=data.get("nextPageToken",None)
        for item in item_data:
            try:
                kind=item['id']['kind']
                if kind=='yoututbe#video':
                    video_id=item['id']['videoId']
                    channel_videos[video_id]=dict()
            except KeyError:
                print("error")
        return channel_videos,nextPageToken
                
        
        
    def dump(self):
        if self.channel_statistics is None:
            return
        
        channel_title="T-Series"
        channel_title=channel_title.replace("-","_").lower()
        filename=channel_title + '.json'
        with open(filename,'w') as f:
            json.dump(self.channel_statistics,f,indent=4)
        print("File Dumped")