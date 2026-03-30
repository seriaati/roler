# pyright: reportAssignmentType=false

from __future__ import annotations

from typing import ClassVar

from tortoise import fields
from tortoise.models import Model


class RolePanel(Model):
    id = fields.IntField(primary_key=True)
    guild_id = fields.BigIntField()
    source_channel_id = fields.BigIntField()
    source_message_id = fields.BigIntField(unique=True)
    target_channel_id = fields.BigIntField()
    target_message_id = fields.BigIntField(unique=True)
    created_by = fields.BigIntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    webhook_id = fields.BigIntField(null=True)
    webhook_token = fields.CharField(max_length=200, null=True)
    webhook_name = fields.CharField(max_length=80, null=True)
    webhook_avatar_url = fields.CharField(max_length=2048, null=True)

    class Meta:
        table = "role_panels"
        indexes: ClassVar = [("source_message_id",)]
