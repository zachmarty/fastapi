from aiogram import Router
from aiogram.types import Message
from fastapi_server.orm import ItemOrm

message_router = Router()

@message_router.message()
async def get_item_by_article(message: Message):
    try:
        text = int(message.text)
    except:
        await message.answer("Please enter product article")
        return
    item = await ItemOrm.get_item(text)
    if item is None:
        await message.answer("Product not found")
        return
    await message.answer(f"Product info\nname: {item.name}\narticle: {item.article}\nprice: {item.price}\namount: {item.amount}")

    
    