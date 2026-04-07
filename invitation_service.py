"""
Invitation Service for Hợp Tuổi viral loop (Sprint 98 — COMP-1/COMP-3).
Sprint 101 ANA-3: A/B message_variant support.

SQLite table: invitations
- id: 8-char URL-safe base62 ID
- initiator_device_id: TEXT
- year_a, year_b: INTEGER
- name_a, name_b: TEXT
- context: TEXT (romance/family/business)
- hop_tuoi_result: TEXT (JSON)
- partner_completed: BOOLEAN DEFAULT 0
- message_variant: TEXT (default/curiosity/urgency) — Sprint 101
- created_at: TIMESTAMP
"""
import json
import secrets
import random
import aiosqlite
from datetime import datetime
from pathlib import Path

_DB_PATH = Path(__file__).parent / "tuvi_invitations.db"

_INVITE_COLUMNS = (
    "id TEXT PRIMARY KEY, initiator_device_id TEXT, "
    "year_a INTEGER, year_b INTEGER, name_a TEXT, name_b TEXT, "
    "context TEXT, hop_tuoi_result TEXT, "
    "partner_completed INTEGER DEFAULT 0, "
    "message_variant TEXT DEFAULT 'default', "
    "created_at TEXT"
)

_VARIANTS = ["default", "curiosity", "urgency"]

_VARIANT_MESSAGES = {
    "default": "[Tên] vừa xem hợp tuổi với bạn! 🌟 Kết quả đang chờ: [link]",
    "curiosity": "Ai đó vừa xem tương hợp với bạn 👀 Bạn có muốn biết kết quả? [link]",
    "urgency": "[Tên] đang chờ bạn xem kết quả hợp tuổi! ⏳ Xem ngay: [link]",
}


async def _get_db() -> aiosqlite.Connection:
    db = await aiosqlite.connect(_DB_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute(
        f"CREATE TABLE IF NOT EXISTS invitations ({_INVITE_COLUMNS})"
    )
    # Sprint 101: add message_variant column to existing tables
    try:
        await db.execute("ALTER TABLE invitations ADD COLUMN message_variant TEXT DEFAULT 'default'")
        await db.commit()
    except Exception:
        pass  # column already exists
    return db


def _short_id() -> str:
    """Generate 8-char URL-safe base62 ID."""
    return secrets.token_hex(4)  # 8 hex chars = 62^8 ≈ 218 trillion combos


async def create_invitation(
    initiator_device_id: str,
    year_a: int, year_b: int,
    name_a: str, name_b: str,
    context: str,
    hop_tuoi_result: dict,
) -> dict:
    """Create invitation. Returns {invitation_id, deep_link, message_variant, message_text}."""
    db = await _get_db()
    try:
        invite_id = _short_id()
        result_json = json.dumps(hop_tuoi_result, ensure_ascii=False)
        now = datetime.utcnow().isoformat()
        # Sprint 101 ANA-3: random variant assignment
        variant = random.choice(_VARIANTS)
        deep_link = f"/hop-tuoi?invite={invite_id}"
        await db.execute(
            "INSERT INTO invitations "
            "(id, initiator_device_id, year_a, year_b, name_a, name_b, "
            "context, hop_tuoi_result, partner_completed, message_variant, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)",
            (invite_id, initiator_device_id, year_a, year_b,
             name_a or "", name_b or "", context, result_json, variant, now)
        )
        await db.commit()
    finally:
        await db.close()

    message_text = _VARIANT_MESSAGES[variant].replace("[link]", deep_link).replace("[Tên]", name_a or "Ai đó")
    return {
        "invitation_id": invite_id,
        "deep_link": deep_link,
        "message_variant": variant,
        "message_text": message_text,
    }


async def get_invitation(invitation_id: str) -> dict | None:
    """Retrieve invitation by ID. Returns dict or None."""
    db = await _get_db()
    try:
        cur = await db.execute(
            "SELECT * FROM invitations WHERE id = ?", (invitation_id,)
        )
        row = await cur.fetchone()
        if row is None:
            return None
        r = dict(row)
        r["hop_tuoi_result"] = json.loads(r["hop_tuoi_result"] or "{}")
        r["partner_completed"] = bool(r["partner_completed"])
        r["message_variant"] = r.get("message_variant", "default")
        return r
    finally:
        await db.close()


async def complete_invitation(invitation_id: str, partner_device_id: str) -> dict | None:
    """Mark invitation as completed by partner. Returns updated dict or None."""
    db = await _get_db()
    try:
        await db.execute(
            "UPDATE invitations SET partner_completed = 1 WHERE id = ?",
            (invitation_id,)
        )
        await db.commit()
        cur = await db.execute(
            "SELECT * FROM invitations WHERE id = ?", (invitation_id,)
        )
        row = await cur.fetchone()
        if row is None:
            return None
        r = dict(row)
        r["hop_tuoi_result"] = json.loads(r["hop_tuoi_result"] or "{}")
        r["partner_completed"] = True
        return r
    finally:
        await db.close()
