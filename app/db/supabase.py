import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

class SupabaseManager:
    def __init__(self):
        self.url: str        = os.getenv("SUPABASE_URL")
        self.anon_key: str   = os.getenv("SUPABASE_ANON_KEY")
        self.service_key:str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

        # Public client for standard API operations.
        self.client: Client  = create_client(self.url, self.anon_key)

    def get_service_client(self) -> Client:
        """
        Returns a client with service_role privileges.
        To be used ONLY by the Batch process to bypass RLS
        :return: Supabase client
        """
        return create_client(self.url, self.service_key)


db_manager = SupabaseManager()
supabase = db_manager.client




