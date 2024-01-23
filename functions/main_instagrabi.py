from instagrapi import Client

class InstagrabiClient:
    def __init__(self, username, password):
        self.client = Client()
        try:
            self.client.login(username, password)
        except Exception as e:
            print(f"Login failed: {e}")

    def get_user_id(self, username):
        return self.client.user_id_from_username(username)

    def get_profile_followers_count(self, username):
        user_id = self.get_user_id(username)
        follower_ids = self.client.user_followers(user_id)
        return len(follower_ids)

    def get_profile_followings_count(self, username):
        user_id = self.get_user_id(username)
        following_ids = self.client.user_following(user_id)
        return len(following_ids)


    def get_total_likes(self, username):
        user_id = self.get_user_id(username)  # Benutzer-ID abrufen
        posts = self.client.user_medias(user_id, amount=0)  # Alle Posts abrufen
        total_likes = sum(post.like_count for post in posts)  # Summe der Likes aller Posts
        return total_likes

    def get_total_comments(self, username):
        user_id = self.get_user_id(username)  # Benutzer-ID abrufen
        posts = self.client.user_medias(user_id, amount=0)  # Alle Posts abrufen
        total_comments = sum(post.comment_count for post in posts)  # Summe der Kommentare aller Posts
        return total_comments