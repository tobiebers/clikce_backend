from TikTokApi import TikTokApi
class TikTokClient:
    def __init__(self):
        self.api = TikTokApi()

    async def get_user_profile(self, username):
        user_info = await self.api.user.info(username)
        return user_info

    async def get_user_followers_count(self, username):
        user_info = await self.get_user_profile(username)
        return user_info.get('stats', {}).get('followerCount', 0)

    async def get_user_followings_count(self, username):
        user_info = await self.get_user_profile(username)
        return user_info.get('stats', {}).get('followingCount', 0)