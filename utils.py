from data_helper import SearchResults, SearchResult


def _format_download_link(filename: str) -> str:
    return f"https://assets.warhammer-community.com/{filename}"


def _format_msg(update: SearchResult) -> str:
    return f"{update.title} (updated {update.last_updated}): {_format_download_link(update.file)}"


def format_msgs(updates: SearchResults) -> list[str]:
    msgs: list[str] = []
    cur_msg = ""

    for update in updates:
        to_add = _format_msg(update)
        if len(cur_msg) + len(to_add) > 1999: # stay within 2000 char limit for discord message
            msgs.append(cur_msg)
            cur_msg = to_add
            continue

        cur_msg = "\n".join([cur_msg, to_add])

    msgs.append(cur_msg)
    return msgs
