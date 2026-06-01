import os
from supabase import create_client

def get_db():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    
    if not url or not key:
        return None
        
    try:
        return create_client(url, key)
    except Exception:
        return None
