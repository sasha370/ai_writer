from typing import Any, Dict

from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults

from graph_types import MainState

web_search_tool = TavilySearchResults(max_result=5, include_answer=False)


def web_search(state: MainState) -> Dict[str,Any]:
    print("--- Web Search ---")
    questions = state["search_queries"]
    documents = state["search_results"]

    for question in questions:
        tavily_results = web_search_tool.invoke({"query": question})
        print(f"SEARCH RESULTS: {tavily_results}")

        joined_tavily_results = '\n'.join(
            [f"Source: {tavily_result["url"]}.\n Text: {tavily_result["content"]}"  for tavily_result in tavily_results]
        )
        print(f"PREPARED DOCS: {joined_tavily_results}")
        # Convert the list of search results into a single document
        web_results = Document(page_content=joined_tavily_results)

        if documents is not None:
            documents.append(web_results)
        else:
            documents = [web_results]

    return {"search_results": documents}
