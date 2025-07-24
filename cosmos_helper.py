from azure.cosmos import CosmosClient, DatabaseProxy, ContainerProxy
from azure.cosmos.exceptions import (
    CosmosResourceNotFoundError,
    CosmosResourceExistsError,
)

from data_helper import SearchResultsModel, SearchResults


class CosmosDBHelper:
    DATABASE_NAME = "monitork-database"
    CONTAINER_NAME = "monitork-container"
    SEARCH_RESULTS_ID = "search_results"
    SEARCH_RESULTS_CATEGORY = "Warhammer40000"

    def __init__(self, conn_string: str) -> None:
        self.client = CosmosClient.from_connection_string(conn_string)
        self.database = self._get_database()
        self.container = self._get_container(self.database)

    def _get_database(self) -> DatabaseProxy:
        try:
            return self.client.get_database_client(self.DATABASE_NAME)
        except CosmosResourceNotFoundError:
            print("Database not found")

        raise Exception("Error finding database")

    def _get_container(self, database: DatabaseProxy) -> ContainerProxy:
        try:
            return database.get_container_client(self.CONTAINER_NAME)
        except CosmosResourceNotFoundError:
            print("Container not found")

        raise Exception("Error finding container")

    def read_prev_downloads(self) -> SearchResults:
        try:
            item = self.container.read_item(
                item=self.SEARCH_RESULTS_ID, partition_key=self.SEARCH_RESULTS_CATEGORY
            )
            return SearchResultsModel.validate_python(item["content"])
        except CosmosResourceNotFoundError:
            print("Item not found when reading")

        raise Exception("Error finding item")

    def update_prev_downloads(self, downloads: SearchResults) -> None:
        try:
            self.container.replace_item(
                item=self.SEARCH_RESULTS_ID,
                body={
                    "id": self.SEARCH_RESULTS_ID,
                    "category": self.SEARCH_RESULTS_CATEGORY,
                    "content": SearchResultsModel.dump_python(downloads),
                },
            )
        except CosmosResourceNotFoundError:
            print("Item not found when updating")

    def create_prev_downloads(self) -> None:
        try:
            self.container.create_item(
                body={
                    "id": self.SEARCH_RESULTS_ID,
                    "category": self.SEARCH_RESULTS_CATEGORY,
                    "content": [],
                }
            )
        except CosmosResourceExistsError:
            print("Item already exists")
