from fastapi import APIRouter
from fastapi_server.orm import ItemOrm, SchedulerORM

# from fastapi_server.management import NoteORM
from fastapi_server.schemas import ItemBase, ArticleBase
import requests


router = APIRouter()

async def get_and_save_product(article : int):
    r = requests.get(
        f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"
    ).json()
    item = ItemBase(
        name=r["data"]["products"][0]["name"],
        article=r["data"]["products"][0]["id"],
        price=r["data"]["products"][0]["priceU"],
        rating=r["data"]["products"][0]["rating"],
        amount=r["data"]["products"][0]["totalQuantity"],
    )
    await ItemOrm.add_or_update_item(item)
    print("executed")

@router.post("/api/v1/products")
async def post_get_and_save_product(article: ArticleBase):
    r = requests.get(
        f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article.article}"
    ).json()
    if len(r["data"]["products"]) == 0:
        return {"data": "not found"}
    item = ItemBase(
        name=r["data"]["products"][0]["name"],
        article=r["data"]["products"][0]["id"],
        price=r["data"]["products"][0]["priceU"],
        rating=r["data"]["products"][0]["rating"],
        amount=r["data"]["products"][0]["totalQuantity"],
    )
    await ItemOrm.add_or_update_item(item)
    return item

@router.get("/api/v1/subscribe/{article}")
async def periodical_get_and_save_product(article : int):
    r = requests.get(
        f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"
    ).json()
    if len(r["data"]["products"]) == 0:
        return {"data": "not found"}
    ans = await SchedulerORM.add_schedule(article)
    print('got', ans)
    if ans == "added":
        from server import scheduler
        scheduler.add_job(get_and_save_product, "interval", minutes = 30, args = [article])
    return {"data": "started"}
    
    
