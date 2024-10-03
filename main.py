from dotenv import load_dotenv

load_dotenv()

from nodes.article_structure_builder import generate_article_structure
from nodes.writer import write_article
from nodes.queries_extractor import generate_search_queries
from nodes.web_search import web_search

from langgraph.graph import StateGraph
from graph_types import MainState

GENERATE_SEARCH_QUERIES = "generate_search_queries"
GENERATE_ARTICLE_STRUCTURE = "generate_article_structure"
WEB_SEARCH = "web_search"
WRITE_ARTICLE = "write_article"

main_graph = StateGraph(MainState)
main_graph.set_entry_point(GENERATE_ARTICLE_STRUCTURE)
main_graph.add_node(GENERATE_ARTICLE_STRUCTURE, generate_article_structure)
main_graph.add_node(GENERATE_SEARCH_QUERIES, generate_search_queries)
main_graph.add_node(WEB_SEARCH, web_search)
main_graph.add_node(WRITE_ARTICLE, write_article)

main_graph.add_edge(GENERATE_ARTICLE_STRUCTURE, GENERATE_SEARCH_QUERIES)
main_graph.add_edge(GENERATE_SEARCH_QUERIES, WEB_SEARCH)
main_graph.add_edge(WEB_SEARCH, WRITE_ARTICLE)

app = main_graph.compile()
# app.get_graph().draw_mermaid_png(output_file_path="graph.png")


def get_user_input():
    user_input = None
    while user_input is None:
        choice = input(
            "How do you want to enter the data? \nPress: \n1: Manual input \n2: Read from a file (create task.txt file in the current folder with your instructions before continue):")

        if choice == '1':
            user_input = input("Input your idea for the article: ")
        elif choice == '2':
            try:
                with open('task.txt', 'r') as file:
                    user_input = file.read()
            except FileNotFoundError:
                print(
                    "File not found. Please create 'task.txt' file in the current folder with your instructions before continue.")
                user_input = None
        else:
            print("----------\nWrong choice. Please try again.")
    return user_input


if __name__ == "__main__":
    print("Let's rock |_(^_^)_/")
    print(
        """
           I can help you with writing an article about any topic.\n
           You can give me a detailed instructions on the contents of the article
           or just give me something to talk about.
        """
    )

    initial_state = MainState(
        user_input=get_user_input(),
        search_queries=None,
        search_results=None,
        article_structure=None,
        article=None
    )
    try:
        res = app.invoke(initial_state)
        if 'article' in res:
            with open('output.txt', 'w') as file:
                file.write(res['article'])
            print("I'm done! Check the output.txt file for the article.")
        else:
            print("No article generated. Please check the state and try again.")
    except Exception as e:
        print(f"I'm so sorry, I encountered an error: {e}")
