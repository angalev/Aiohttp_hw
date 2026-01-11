# app.py
from __future__ import annotations
from aiohttp import web
from models import Advertisement, Session, Base, engine
from errors import HttpError
from schema import validate, CreateAdvertisementRequest


def get_advertisement(ad: Advertisement | None, ad_id: int):
    if ad is None:
        raise HttpError(404, "advertisement not found")
    return ad


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except HttpError as e:
        return web.json_response(
            {"error": e.message},
            status=e.status_code
        )


async def get_ad(request: web.Request):
    ad_id = int(request.match_info["ad_id"])
    with Session() as session:
        ad = session.get(Advertisement, ad_id)
        ad = get_advertisement(ad, ad_id)
        return web.json_response(ad.json)


async def create_ad(request: web.Request):
    json_data = await request.json()
    validated_data = validate(CreateAdvertisementRequest, json_data)
    with Session() as session:
        ad = Advertisement(**validated_data)
        session.add(ad)
        session.commit()
        session.refresh(ad)
        return web.json_response(ad.json)


async def delete_ad(request: web.Request):
    ad_id = int(request.match_info["ad_id"])
    with Session() as session:
        ad = session.get(Advertisement, ad_id)
        ad = get_advertisement(ad, ad_id)
        session.delete(ad)
        session.commit()
        return web.json_response({"status": "deleted"})


app = web.Application(middlewares=[error_middleware])

# Создаём таблицы при старте
Base.metadata.create_all(engine)

# Маршруты
app.add_routes(
    [
        web.get("/ad/{ad_id:\d+}", get_ad),
        web.post("/ad", create_ad),
        web.delete("/ad/{ad_id:\d+}", delete_ad),
    ]
)

if __name__ == "__main__":
    web.run_app(app, host="127.0.0.1", port=5000)