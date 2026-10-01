from supabase import acreate_client, AsyncClient
from app.config import SUPABASE_URL, SUPABASE_KEY

_client: AsyncClient | None = None


async def get_supabase() -> AsyncClient:
    global _client
    if _client is None:
        _client = await acreate_client(SUPABASE_URL, SUPABASE_KEY)
    return _client