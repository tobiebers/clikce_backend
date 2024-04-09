from instagrapi import Client
from instagrapi.exceptions import ClientError

class InstagrabiClient:
    def __init__(self, username, password):
        self.client = Client()
        try:
            self.client.login(username, password)
        except ClientError as e:
            print(f"Login failed: {e}")

    def get_user_id(self, username):
        return self.client.user_id_from_username(username)

    def get_profile_info(self, username):
        """Holt grundlegende Profilinformationen."""
        user_info = self.client.user_info_by_username(username)
        return {
            "profile_pic_url": user_info.profile_pic_url,
            "full_name": user_info.full_name,
            "username": user_info.username,
            "followers_count": user_info.follower_count,
            "followings_count": user_info.following_count,
            "total_likes": self.get_total_likes(username),
        }

    def get_total_likes(self, username):
        """Holt die Gesamtanzahl der Likes für alle Posts eines Benutzers."""
        user_id = self.get_user_id(username)
        posts = self.client.user_medias(user_id, amount=0)
        return sum(post.like_count for post in posts)

    def get_total_comments(self, username):
        """Holt die Gesamtanzahl der Kommentare für alle Posts eines Benutzers."""
        user_id = self.get_user_id(username)
        posts = self.client.user_medias(user_id, amount=0)
        return sum(post.comment_count for post in posts)

    def get_top_post_details(self, username):
        """Holt Details des Posts mit den meisten Likes."""
        user_id = self.get_user_id(username)
        posts = self.client.user_medias(user_id, amount=50)
        top_post = max(posts, key=lambda post: post.like_count, default=None)

        if top_post:
            top_comment = max(top_post.comments, key=lambda comment: comment.like_count, default=None)
            return {
                "post_image_url": top_post.media_url,
                "description": top_post.caption_text,
                "hashtags": top_post.caption_hashtags,
                "likes": top_post.like_count,
                "comments_count": top_post.comment_count,
                "top_comment": top_comment.text if top_comment else None
            }
        return None
