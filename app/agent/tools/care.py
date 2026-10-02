from typing import Literal
from app.services.supabase import get_supabase
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

def make_care_tools(user_id: str) -> dict:
    async def get_today_tasks() -> list[dict]:
        """Возвращает задачи по уходу, которые пора выполнить сегодня или которые уже просрочены (он уже содержит имена растений)"""
        db = await get_supabase()
        res = await (
            db.table("care_tasks")
            .select("id, type, interval_days, last_done_at, plant_id, plants(name, is_archived)")
            .eq("user_id", user_id)
            .execute()
        )
        now = datetime.now(timezone.utc)
        tasks = []

        for row in res.data:
            plant = row["plants"] or {}
            if plant.get("is_archived"):
                continue  # архивные растения пропускаем

            if row["last_done_at"] is None:
                overdue_days = None  # ни разу не делали
            else:
                due_at = datetime.fromisoformat(row["last_done_at"]) + timedelta(days=row["interval_days"])
                if due_at > now:
                    continue  # срок ещё не наступил
                overdue_days = (now - due_at).days

            tasks.append({
                "task_id": row["id"],
                "plant_id": row["plant_id"],
                "plant_name": plant.get("name"),
                "type": row["type"],
                "never_done": row["last_done_at"] is None,
                "overdue_days": overdue_days,
            })

        return tasks

    async def mark_task_done(
            plant_id: str,
            care_type: Literal["watering", "misting", "feeding"],
    ) -> dict:
        """Отмечает уход за растением выполненным и записывает это в историю ухода.
        care_type: watering — полив, misting — опрыскивание, feeding — подкормка.
        Используй, когда пользователь сообщает, что уже сделал уход.
        Отметить можно в любой момент, даже раньше срока.
        """
        db = await get_supabase()
        now = datetime.now(timezone.utc).isoformat()

        res = await (
            db.table("care_tasks")
            .update({"last_done_at": now})
            .eq("user_id", user_id)
            .eq("plant_id", plant_id)
            .eq("type", care_type)
            .execute()
        )

        if not res.data:
            raise ValueError("У этого растения нет задачи такого типа")

        return {"plant_id": plant_id, "care_type": care_type, "done_at": now}

    async def get_watering_history(plant_id: str) -> list[str]:
        """Возвращает даты последних поливов растения по его id"""
        db = await get_supabase()

        res = await (
            db.table("plant_care_logs")
            .select("performed_at")
            .eq("user_id", user_id)
            .eq("plant_id", plant_id)
            .eq("type", "watering")
            .order("performed_at", desc=True)
            .limit(10)
            .execute()
        )

        return [
            datetime.fromisoformat(row["performed_at"]).astimezone(ZoneInfo("Europe/Moscow")).isoformat()
            for row in res.data
        ]

    return {
        "get_today_tasks": get_today_tasks,
        "mark_task_done": mark_task_done,
        "get_watering_history": get_watering_history,
    }
