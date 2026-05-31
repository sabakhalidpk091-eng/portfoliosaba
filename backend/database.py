import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in the environment")

_supabase_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def get_db():
    """Return the initialized Supabase client."""
    return _supabase_client
