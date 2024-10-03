from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from graph_types import MainState


class PreparedParams(BaseModel):
    prepared_questions: list[str]

llm = ChatOpenAI(model="gpt-4o-mini")


# Imagine you are a research specialist dedicated to crafting precise search queries for technical assignments. I need you to thoroughly analyze the user input text to identify key information gaps and generate relevant search queries that will collect essential data from credible sources on the Internet. Each query should be specific, actionable, and aimed at acquiring detailed insights or data points needed for the technical assignment. Output your response in a structured JSON format with each query listed.
# Assume the role of an expert in generating Internet search queries for technical research. Your task is to assess the user's input text and create a targeted list of queries designed to find information that will support the development of a technical assignment. Ensure the queries are precise, varied, and cover different aspects such as technical specifications, user requirements, industry benchmarks, and similar projects. Present the output in JSON format, with each query clearly defined for optimal search results.

system = """
You are an expert research assistant specializing in generating precise search queries.
 Your task is to analyze the provided `C` for a technical assignment and the `article_structure` 
 to create a comprehensive list of search queries. 
 These queries should be designed to gather all necessary information from the Internet to fulfill the requirements 
 of the assignment and to develop the article according to the given structure.
  Ensure each query is specific, actionable, and directly related to the content needs outlined in both the `instructions` 
  and the `article_structure`.
   Present your response in JSON format with each query clearly defined for optimal search results.
   Begin!
   Instructions: {instruction}
   Article structure: {article_structure}

"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Here is a user input: {instruction} and article structure: {article_structure}"),
    ]
)

llm_with_schema = llm.with_structured_output(schema=PreparedParams)
generate_instruction_chain = prompt | llm_with_schema

def generate_search_queries(state: MainState) -> dict:
    user_input = state["user_input"]
    article_structure = state["article_structure"]

    response = generate_instruction_chain.invoke({"instruction": user_input, "article_structure": article_structure})
    print(f"Generated questions: {response.prepared_questions}")

    return {"search_queries": response.prepared_questions}
