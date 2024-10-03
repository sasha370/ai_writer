from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from graph_types import MainState


class ArticleStructure(BaseModel):
    article_structure: str

llm = ChatOpenAI(model="gpt-4o-mini")


system = """
 You are an expert article structure planner. Your task is to carefully analyze a provided technical assignment for
  writing an article and develop a detailed structure for the future article. 
  The structure should include key sections, headings, and subheadings, with a brief description of what each section will cover. 
  Ensure the structure aligns with the requirements of the technical assignment, focusing on clarity, logical flow, and completeness of the content. 
  Present the structure in an organized format that can serve as a clear guide for the article's development.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Here is a user input: {instruction}"),
    ]
)

# llm_with_schema = llm.with_structured_output(schema=ArticleStructure)
generate_task_chain = prompt | llm

def generate_article_structure(state: MainState) -> dict:
    user_input = state["user_input"]

    response = generate_task_chain.invoke({"instruction": user_input})
    print(f"Generated article structure: {response.content}")

    return {"article_structure": response.content}
