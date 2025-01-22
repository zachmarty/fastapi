from fastapi_server.schemas import ItemBase
from fastapi_server.models import new_session, Item
from sqlalchemy import select

class ItemOrm:

    @classmethod
    async def get_item(cls, article):
        async with new_session() as session:
            query = select(Item).where(Item.article == article)
            result = await session.execute(query)
            item = result.scalars().first()
            return item

    @classmethod
    async def add_or_update_item(cls, data : ItemBase):
        item = await ItemOrm.get_item(data.article)
        async with new_session() as session:
            data_dict = data.model_dump()
            if item is None:
                new_item = Item(**data_dict)
                session.add(new_item)
                await session.flush()
                await session.commit()
                return "ok"
            for key, val in data_dict.items():
                setattr(item, key, val)
            await session.flush()
            await session.commit()
            return "ok"
        

    
