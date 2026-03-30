from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0001_initial')]

    initial = False

    operations = [
        ops.AddField(
            model_name='RolePanel',
            name='webhook_avatar_url',
            field=fields.CharField(null=True, max_length=2048),
        ),
        ops.AddField(
            model_name='RolePanel',
            name='webhook_id',
            field=fields.BigIntField(null=True),
        ),
        ops.AddField(
            model_name='RolePanel',
            name='webhook_name',
            field=fields.CharField(null=True, max_length=80),
        ),
        ops.AddField(
            model_name='RolePanel',
            name='webhook_token',
            field=fields.CharField(null=True, max_length=200),
        ),
    ]
