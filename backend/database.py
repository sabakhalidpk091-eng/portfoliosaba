import os
from supabase import create_client, Client

# Singleton pattern to reuse connection
_db: Client = None

def get_db() -> Client:
    global _db
    if _db is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        if not url or not key:
            # For local dev if os.getenv fails to pick it up immediately
            try:
                from config import settings
                url = settings.SUPABASE_URL
                key = settings.SUPABASE_ANON_KEY
            except:
                pass
        
        if not url or not key:
             raise ValueError("SUPABASE_URL or SUPABASE_ANON_KEY is not set.")
             
        _db = create_client(url, key)
    return _db
