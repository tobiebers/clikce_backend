import instaloader

class InstaloaderClient:
    def __init__(self):
        self.loader = instaloader.Instaloader()

    def get_profile(self, username):
        return instaloader.Profile.from_username(self.loader.context, username)

    def get_profile_followers(self, profile):
        return profile.followers

    def get_profile_posts(self, username):
        profile = self.get_profile(username)
        posts = []
        for post in profile.get_posts():
            posts.append({
                "caption": post.caption,
                "image_url": post.url,
                "date_posted": post.date,
                "likes": post.likes,  # Anzahl der Likes
                # ... Weitere Informationen je nach Bedarf
            })
        return posts


