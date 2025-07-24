from data_helper import get_downloads, get_updated_downloads
from discord_helper import post_updates
from utils import format_msgs
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


from cosmos_helper import CosmosDBHelper


DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    token: str
    cosmos_conn_string: str
    model_config = SettingsConfigDict(env_file=DOTENV)


if __name__ == "__main__":
    settings = Settings()
    new_downloads = get_downloads()

    db = CosmosDBHelper(settings.cosmos_conn_string)
    prev_downloads = db.read_prev_downloads()

    updated_downloads = get_updated_downloads(prev_downloads, new_downloads)
    if len(updated_downloads) > 0:
        msgs = format_msgs(updated_downloads)
        post_updates(msgs, settings.token)
    else:
        print("Found no updates")

    db.update_prev_downloads(new_downloads)
