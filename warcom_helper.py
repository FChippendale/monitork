import requests
import json
from typing import TypeAlias
from pydantic import BaseModel, TypeAdapter


class SearchResult(BaseModel):
    title: str
    created_at: str  # e.g. 11/12/2024
    last_updated: str  # e.g. 11/12/2024
    # new: bool  # commented out as was causing false positives. Not clear what it means to be marked as "new"
    file: str
    file_size: str


class Hit(BaseModel):
    title: str
    id: SearchResult


class Data(BaseModel):
    hits: list[Hit]


SearchResults: TypeAlias = list[SearchResult]
SearchResultsModel = TypeAdapter(SearchResults)


def _filter_downloads(results: SearchResults) -> SearchResults:
    filtered_results = []
    for r in results:
        if r.title.startswith("Legends"):
            continue

        if r.title.startswith("Combat Patrol"):
            continue

        if r.title.startswith("Boarding Actions"):
            continue

        if r.title.startswith("Horus Heresy Legends"):
            continue

        filtered_results.append(r)

    return filtered_results


def get_downloads() -> SearchResults:
    url = "https://www.warhammer-community.com/api/search/downloads/"
    payload = {
        "index": "downloads_v2",
        "searchTerm": "",
        "gameSystem": "warhammer-40000",
        "language": "english",
    }

    response = requests.post(url, data=json.dumps(payload))
    response.raise_for_status()

    parsed_data = Data.model_validate(response.json())
    return _filter_downloads([d.id for d in parsed_data.hits])


def get_updated_downloads(prev: SearchResults, new: SearchResults) -> SearchResults:
    updated: SearchResults = []

    for item in new:
        if item not in prev:
            print("Item updated:", item)
            updated.append(item)

            # simple search to create better logs for items marked as updated
            for prev_item in prev:
                if prev_item.title == item.title:
                    print("Prev item with matching title:", prev_item)

    return updated
