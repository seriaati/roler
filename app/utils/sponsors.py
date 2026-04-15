import aiohttp
from loguru import logger

from app.core.settings import SETTINGS


async def is_sponsor(user_id: int) -> bool:
    if SETTINGS.sponsor_api_key is None:
        return True

    try:
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                "https://api.seria.moe/sponsors", headers={"x-api-key": SETTINGS.sponsor_api_key}
            ) as resp,
        ):
            resp.raise_for_status()
            sponsors: list[dict[str, str]] = await resp.json()
            return any(s.get("id") == str(user_id) for s in sponsors)
    except Exception as e:
        logger.warning(f"Sponsor check failed for user {user_id}: {e}")
        return False
