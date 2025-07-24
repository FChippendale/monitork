import requests
import json
from typing import TypeAlias
from pydantic import BaseModel, TypeAdapter
from enum import StrEnum
import os


URL = "https://www.warhammer-community.com/api/search/downloads/"
PAYLOAD = {
    "index": "downloads_v2",
    "searchTerm": "",
    "gameSystem": "warhammer-40000",
    "language": "english",
}


class SearchResult(BaseModel):
    title: str
    created_at: str    # e.g. 11/12/2024
    last_updated: str  # e.g. 11/12/2024
    new: bool
    file: str
    file_size: str


class Hit(BaseModel):
    title: str
    id: SearchResult


class Data(BaseModel):
    hits: list[Hit]


SearchResults: TypeAlias = list[SearchResult]
SearchResultsModel = TypeAdapter(SearchResults)


class File(StrEnum):
    ALL_RESULTS = "results.json"
    UPDATED_RESULTS = "updates.json"


def read_json(file: File) -> SearchResults:
    with open(file.value, "r") as file:
        prev_search_string = json.load(file)

    return SearchResultsModel.validate_python(prev_search_string)


def write_json(file: File, results: SearchResults) -> None:
    with open(file.value, "w") as fp:
        json.dump(SearchResultsModel.dump_python(results), fp)


def get_download_link(filename: str) -> str:
    return f"https://assets.warhammer-community.com/{filename}"


def get_downloads() -> list[SearchResult]:
    response = requests.post(URL, data=json.dumps(PAYLOAD))
    response.raise_for_status()

    parsed_data = Data.model_validate(response.json())
    return [d.id for d in parsed_data.hits]


def compare_downloads(results: SearchResults) -> bool:
    if os.path.isfile(File.ALL_RESULTS):
        prev_results = read_json(File.ALL_RESULTS)
    else: 
        prev_results = results

    changed_results: SearchResults = []
    for result in results:
        if result not in prev_results:
            changed_results.append(result)

    write_json(File.ALL_RESULTS, results)
    write_json(File.UPDATED_RESULTS, changed_results)

    return len(changed_results) > 0

