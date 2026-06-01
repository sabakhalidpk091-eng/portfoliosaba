from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

# Initialize once at module level (Cold Start)
def _init_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        return None
    
    # Custom options to avoid connection pooling issues on Vercel
    opts = ClientOptions(postgrest_client_timeout=10)
    return create_client(url, key, options=opts)

_db_instance = _init_client()

def get_db() -> Client:
    if _db_instance is None:
        # Retry once if it was None (mostly for local dev)
        return _init_client()
    return _db_instance
