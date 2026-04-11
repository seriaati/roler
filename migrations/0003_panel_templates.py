from tortoise import migrations
from tortoise.migrations import operations as ops


class Migration(migrations.Migration):
    dependencies = [("models", "0002_auto_20260330_2201")]

    initial = False

    operations = [
        ops.RunSQL(
            sql="""
CREATE TABLE IF NOT EXISTS "panel_templates" (
    "id" SERIAL PRIMARY KEY,
    "guild_id" BIGINT NOT NULL,
    "template_id" VARCHAR(64) NOT NULL,
    "source_channel_id" BIGINT NOT NULL,
    "source_message_id" BIGINT NOT NULL UNIQUE,
    "content" TEXT NOT NULL,
    "created_by" BIGINT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE ("guild_id", "template_id")
);
CREATE INDEX IF NOT EXISTS "idx_panel_templates_guild_template"
    ON "panel_templates" ("guild_id", "template_id");
""",
            reverse_sql='DROP TABLE IF EXISTS "panel_templates";',
        ),
    ]
