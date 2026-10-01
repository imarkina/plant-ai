from app.services.supabase import get_supabase
from datetime import datetime, timedelta, timezone


def make_care_tools(user_id: str) -> dict:
    async def get_today_tasks() -> list[dict]:
        """Возвращает задачи по уходу, которые пора выполнить сегодня или которые уже просрочены"""
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

    return {
        "get_today_tasks": get_today_tasks
    }
