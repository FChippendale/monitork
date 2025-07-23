from data_helper import get_downloads, compare_downloads
from discord_helper import post_updates


if __name__ == "__main__":
    data = get_downloads()
    if compare_downloads(data):
        post_updates()
