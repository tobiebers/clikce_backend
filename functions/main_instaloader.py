import instaloader

class InstaloaderClient:
    def __init__(self, username, password):
        self.loader = instaloader.Instaloader()
        # Versuchen Sie, sich mit den bereitgestellten Anmeldeinformationen anzumelden
        try:
            self.loader.login(username, password)
        except Exception as e:
            print(f"Fehler bei der Anmeldung: {e}")
            # Optional: Behandeln Sie den Fehler oder brechen Sie ab

    def get_profile(self, username):
        return instaloader.Profile.from_username(self.loader.context, username)

    def get_profile_followers(self, username):
        profile = self.get_profile(username)
        return profile.followers

    def get_profile_posts(self, username):
        profile = self.get_profile(username)
        posts = []
        for post in profile.get_posts():
            comment_count = len(list(post.get_comments()))
            posts.append({
                "caption": post.caption,
                "image_url": post.url,
                "date_posted": post.date,
                "likes": post.likes,
                "comment_count": comment_count,

            })
        return posts

    def get_profile_followings(self, username):
        profile = self.get_profile(username)
        followings = profile.get_followees()
        return len(list(followings))
