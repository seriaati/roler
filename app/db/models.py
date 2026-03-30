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

    class Meta:
        table = "role_panels"
        indexes: ClassVar = [("source_message_id",)]
