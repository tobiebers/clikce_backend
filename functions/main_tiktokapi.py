from TikTokApi import TikTokApi

class TikTokClient:
    def __init__(self):
        self.api = TikTokApi.get_instance()

    def get_user_profile(self, username):
        user_info = self.api.get_user(username)
        return user_info

    def get_user_videos(self, username):
        user_videos = self.api.by_username(username, count=50)  # Anzahl der abzurufenden Videos
        return user_videos

    def get_user_followers_count(self, username):
        user_info = self.get_user_profile(username)
        return user_info['stats']['followerCount']

    def get_user_followings_count(self, username):
        user_info = self.get_user_profile(username)
        return user_info['stats']['followingCount']

    def get_user_likes_count(self, username):
        user_info = self.get_user_profile(username)
        return user_info['stats']['heartCount']

    def get_video_comments_count(self, video_id):
        video_info = self.api.get_video_by_id(video_id)
        return video_info['stats']['commentCount']

    def get_user_videos_with_comments(self, username):
        user_videos = self.get_user_videos(username)
        videos_with_comments = []
        for video in user_videos:
            video_id = video['id']
            comments_count = self.get_video_comments_count(video_id)
            video_data = {
                "video_id": video_id,
                "comments_count": comments_count,
                # ... andere Video-Informationen nach Bedarf
            }
            videos_with_comments.append(video_data)
        return videos_with_comments
