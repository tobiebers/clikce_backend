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

    def get_profile_followers_count(self, username):
        """Holt die Anzahl der Follower eines Benutzers."""
        user_id = self.get_user_id(username)
        user_info = self.client.user_info(user_id)
        return user_info.follower_count

    def get_profile_followings_count(self, username):
        """Holt die Anzahl der Personen, denen ein Benutzer folgt."""
        user_id = self.get_user_id(username)
        user_info = self.client.user_info(user_id)
        return user_info.following_count

    def get_top_post_details(self, username):
        """Holt Details des Posts mit den meisten Likes."""
        user_id = self.get_user_id(username)
        posts = self.client.user_medias(user_id, amount=50)
        top_post = max(posts, key=lambda post: post.like_count, default=None)

        if not top_post:
            # Kein Top-Post gefunden, gebe eine Struktur mit None-Werten zurück
            return {
                "post_image_url": None,
                "description": None,
                "hashtags": [],
                "likes": 0,
                "comments_count": 0,
                "top_comment": None
            }

        # Überprüfe, ob das top_post-Objekt die notwendigen Attribute hat
        top_comment_text = None
        if hasattr(top_post, 'comments') and top_post.comments:
            # Extrahiere den Top-Kommentar, falls vorhanden
            top_comment = max(top_post.comments, key=lambda comment: comment.like_count, default=None)
            top_comment_text = top_comment.text if top_comment else None

        # Bereite die Daten vor, auch wenn einige fehlen könnten
        return {
            "post_image_url": getattr(top_post, 'media_url', None),
            "description": getattr(top_post, 'caption_text', ''),
            "hashtags": getattr(top_post, 'caption_hashtags', []),
            "likes": getattr(top_post, 'like_count', 0),
            "comments_count": getattr(top_post, 'comment_count', 0),
            "top_comment": top_comment_text
        }

