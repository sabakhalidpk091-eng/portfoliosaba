import os
from supabase import create_client

def get_db():
    url = os.environ.get("SUPABASE_URL")
    # Prefer service role key for server operations, fall back to anon key
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_ANON_KEY")
    
    if not url or not key:
        return None
        
    try:
        return create_client(url, key)
    except Exception:
        return None
