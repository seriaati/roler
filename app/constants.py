import datetime

UTC8 = datetime.timezone(datetime.timedelta(hours=8))

WEBHOOK_SPONSOR_MESSAGE = (
    "💎 **Webhooks are a sponsor-only feature.**\n\n"
    "Custom webhook identities (the `[webhook]` tag) require an active sponsorship.\n\n"
    "**To unlock:**\n"
    "1. [Donate here](<https://link.seria.moe/donate>)\n"
    "2. Add [Seria's bot](<https://discord.com/oauth2/authorize?client_id=1556526314167468132>) to your account "
    "or join the [Discord server](<https://link.seria.moe/hb-dc>), then use `/claim`\n\n"
    "Your panel will still work without the `[webhook]` tag, it'll just post as the bot."
)
