from typing import TYPE_CHECKING

from loguru import logger

from app.core.embeds import ErrorEmbed

if TYPE_CHECKING:
    from app.types import Interaction


async def handle_error(i: Interaction, error: Exception) -> None:
    original = getattr(error, "original", None)
    e = original or error
    logger.exception("Error occurred", exc_info=e)
    embed = ErrorEmbed(
        title="An error occurred",
        description="An unexpected error occurred. Please try again later.\nIf the problem persists, please contact the developer.",
    )

    if i.response.is_done():
        await i.followup.send(embed=embed, ephemeral=True)
    else:
        await i.response.send_message(embed=embed, ephemeral=True)
