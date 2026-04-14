from tortoise import migrations
from tortoise.migrations import operations as ops


class Migration(migrations.Migration):
    dependencies = [("models", "0003_panel_templates")]

    initial = False

    operations = [
        ops.RunSQL(
            sql='ALTER TABLE "panel_templates" ADD COLUMN IF NOT EXISTS "stateful" BOOLEAN NOT NULL DEFAULT FALSE;',
            reverse_sql='ALTER TABLE "panel_templates" DROP COLUMN IF EXISTS "stateful";',
        )
    ]
