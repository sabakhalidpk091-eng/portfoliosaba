import os
from supabase import create_client, Client

# Global client
_client = None

def get_db():
    global _client
    if _client is not None:
        return _client
        
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        return None
        
    try:
        _client = create_client(url, key)
        return _client
    except Exception:
        return None
