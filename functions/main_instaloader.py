import instaloader

class InstaloaderClient:
    def __init__(self):
        self.loader = instaloader.Instaloader()



    def display_profile_name(self, profile):
        print("Profilname:", profile.username)

    def display_profile_Follower(self, profile):
        print("Follower:", profile.followers)

    def display_profile_Followeed(self, profile):
        print("Gefolgt von:", profile.followees)


    def extract_post_metadata(self, profile):
        for post in profile.get_posts():
            print("Post:", post.url)
            print("Likes:", post.likes)
            print("Datum:", post.date)
            print("Beschreibung:", post.caption)

# Beispiel für die Verwendung der Klasse
client = InstaloaderClient()
username = 'your_username_here'


