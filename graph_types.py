from typing import TypedDict

from langchain_core.documents import Document


# @dataclass
class MainState(TypedDict):
    """
    Represents the state of the graph.
    """
    user_input: str
    article_structure: str | None
    search_queries: list[str] | None
    search_results: list[Document] | None
    article: str | None

