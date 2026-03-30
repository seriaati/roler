from tortoise import migrations
from tortoise.migrations import operations as ops


class Migration(migrations.Migration):
    dependencies = [("models", "0001_initial")]

    initial = False

    operations = [
        ops.RunSQL(
            sql='ALTER TABLE "role_panels" ADD COLUMN IF NOT EXISTS "webhook_avatar_url" VARCHAR(2048) NULL;',
            reverse_sql='ALTER TABLE "role_panels" DROP COLUMN IF EXISTS "webhook_avatar_url";',
        ),
        ops.RunSQL(
            sql='ALTER TABLE "role_panels" ADD COLUMN IF NOT EXISTS "webhook_id" BIGINT NULL;',
            reverse_sql='ALTER TABLE "role_panels" DROP COLUMN IF EXISTS "webhook_id";',
        ),
        ops.RunSQL(
            sql='ALTER TABLE "role_panels" ADD COLUMN IF NOT EXISTS "webhook_name" VARCHAR(80) NULL;',
            reverse_sql='ALTER TABLE "role_panels" DROP COLUMN IF EXISTS "webhook_name";',
        ),
        ops.RunSQL(
            sql='ALTER TABLE "role_panels" ADD COLUMN IF NOT EXISTS "webhook_token" VARCHAR(200) NULL;',
            reverse_sql='ALTER TABLE "role_panels" DROP COLUMN IF EXISTS "webhook_token";',
        ),
    ]
