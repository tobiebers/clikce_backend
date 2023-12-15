import instaloader

# Erstellen Sie eine Instanz von Instaloader
L = instaloader.Instaloader()

# Profile herunterladen
profile = instaloader.Profile.from_username(L.context, '')

# Informationen zum Profil anzeigen
print("Profilname:", profile.username)
print("Follower:", profile.followers)
print("Gefolgt von:", profile.followees)

# Beiträge herunterladen und Metadaten extrahieren
for post in profile.get_posts():
    print("Post:", post.url)
    print("Likes:", post.likes)
    print("Datum:", post.date)
    print("Beschreibung:", post.caption)

# Beiträge herunterladen und speichern
L.download_profile(profile.username, profile_pic_only=False)
