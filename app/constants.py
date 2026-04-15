import datetime

UTC8 = datetime.timezone(datetime.timedelta(hours=8))

WEBHOOK_SPONSOR_MESSAGE = (
    "💎 **Webhooks are a sponsor-only feature.**\n\n"
    "Custom webhook identities (the `[webhook]` tag) require an active sponsorship.\n\n"
    "**To unlock:**\n"
    "1. [Donate here](<https://link.seria.moe/donate>)\n"
    "2. Contact [Seria on Discord](<https://discord.com/users/410036441129943050>) to activate\n\n"
    "Your panel will still work without the `[webhook]` tag, it'll just post as the bot."
)
