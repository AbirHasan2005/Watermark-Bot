# (c) @doreamonfans1

import datetime
import motor.motor_asyncio

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
    def new_user(self, id):
        return dict(
            id = id,
            join_date = datetime.date.today().isoformat(),
            watermark_position = "5:5",
            watermark_size = "7"
        )
    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return True if user else False
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
    async def set_position(self, id, watermark_position):
        await self.col.update_one({'id': id}, {'$set': {'watermark_position': watermark_position}})
    async def get_position(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('watermark_position', '5:5')
    async def set_size(self, id, watermark_size):
        await self.col.update_one({'id': id}, {'$set': {'watermark_size': watermark_size}})
    async def get_size(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('watermark_size', '7')
