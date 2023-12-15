import instaloader

class InstaloaderClient:
    def __init__(self):
        self.loader = instaloader.Instaloader()

    def get_profile(self, username):
        return instaloader.Profile.from_username(self.loader.context, username)

    def get_profile_followers(self, profile):
        return profile.followers

# Beispiel für die Verwendung der Klasse
client = InstaloaderClient()
username = 'tobi_ebers'

# Profil laden
profile = client.get_profile(username)

# Follower anzeigen
client.get_profile_followers(profile)
