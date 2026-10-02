from app.services.supabase import get_supabase


def make_plant_tools(user_id: str) -> dict:
    async def list_plants() -> list[dict]:
        """Возвращает список растений пользователя: id, имя и вид."""
        db = await get_supabase()
        res = await (
            db.table("plants")
            .select("id, name, custom_species_name, species(common_name)")
            .eq("user_id", user_id)
            .eq("is_archived", False)
            .execute()
        )
        rows = res.data
        return [
            {
                "id": row["id"],
                "name": row["name"],
                "species": (row["species"] or {}).get("common_name") or row["custom_species_name"],
            }
            for row in rows
        ]

    async def get_user_location() -> str:
        """Возвращает город пользователя"""
        return 'Москва'

    async def get_plant_info(plant_id: int) -> dict:
        """Возвращает информацию о растении по его id: вид, горшок, расположение."""
        print(f">>> Вызвана get_plant_info(plant_id={plant_id})")

        if plant_id != 42:
            raise ValueError(f'Растение с plant_id={plant_id} не найдено')

        return {"species": "Hoya carnosa", "pot": "пластик без дренажа", "location": "северное окно"}

    return {
        "get_plant_info": get_plant_info,
        "get_user_location": get_user_location,
        "list_plants": list_plants,
    }
