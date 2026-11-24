import datetime

UTC8 = datetime.timezone(datetime.timedelta(hours=8))

WEBHOOK_SPONSOR_MESSAGE = (
    "💎 **Webhooks are a sponsor-only feature.**\n\n"
    "Custom webhook identities (the `[webhook]` tag) require a sponsorship.\n\n"
    "For ways to sponsor and how to claim perks, visit [sponsor.seria.moe](<https://sponsor.seria.moe>).\n\n"
    "Your panel will still work without the `[webhook]` tag, it'll just post as the bot."
)
