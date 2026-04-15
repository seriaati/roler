# Self-Hosting

## Requirements

- Python 3.14+
- PostgreSQL

## Environment Variables

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_bot_token
ENV=prod

POSTGRES_PASSWORD=your_password
POSTGRES_DB=roler
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres

# Optional: remove to unlock all features for self-hosters
SPONSOR_API_KEY=your_sponsor_api_key
```

| Variable | Description |
|---|---|
| `DISCORD_TOKEN` | Your bot's token from the [Discord Developer Portal](https://discord.com/developers/applications) |
| `ENV` | Set to `prod` for production, `dev` for development |
| `POSTGRES_PASSWORD` | PostgreSQL user password |
| `POSTGRES_DB` | Database name |
| `POSTGRES_HOST` | PostgreSQL host (e.g. `localhost`) |
| `POSTGRES_PORT` | PostgreSQL port (default: `5432`) |
| `POSTGRES_USER` | PostgreSQL username |
| `SPONSOR_API_KEY` | *(Optional)* API key for sponsor verification. If not set, all features are unlocked. |

## Running Locally

```bash
uv sync
uv run main.py
```

## Running with Docker

```bash
docker build -t roler .
docker run --env-file .env roler
```
