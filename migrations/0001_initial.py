from tortoise import migrations
from tortoise.migrations import operations as ops


class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS "role_panels" (
                "id" SERIAL PRIMARY KEY,
                "guild_id" BIGINT NOT NULL,
                "source_channel_id" BIGINT NOT NULL,
                "source_message_id" BIGINT NOT NULL UNIQUE,
                "target_channel_id" BIGINT NOT NULL,
                "target_message_id" BIGINT NOT NULL UNIQUE,
                "created_by" BIGINT NOT NULL,
                "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
            CREATE INDEX IF NOT EXISTS "idx_role_panels_source_message_id"
                ON "role_panels" ("source_message_id");
            """,
            reverse_sql='DROP TABLE IF EXISTS "role_panels";',
        ),
    ]
