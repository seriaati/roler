from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields
from tortoise.indexes import Index

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='RolePanel',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('guild_id', fields.BigIntField()),
                ('source_channel_id', fields.BigIntField()),
                ('source_message_id', fields.BigIntField(unique=True)),
                ('target_channel_id', fields.BigIntField()),
                ('target_message_id', fields.BigIntField(unique=True)),
                ('created_by', fields.BigIntField()),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'role_panels', 'app': 'models', 'indexes': [Index(fields=['source_message_id'])], 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
