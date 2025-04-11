from os import environ

DB_STRING = environ.get("DB_URL", "postgresql+asyncpg://camabeel@localhost/leads")