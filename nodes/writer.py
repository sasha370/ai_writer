from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, BasePromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from graph_types import MainState
from langchain_community.tools.tavily_search import TavilySearchResults

llm = ChatOpenAI(model="gpt-4o")

tools = [TavilySearchResults(max_results=3, name='search')]

react_prompt = PromptTemplate.from_template("""
    Objective: Your task is to write a comprehensive article based on the provided article_structure and relevant context documents.
     Use the structure as a guide to organize the content logically and ensure that each section covers the intended topics.

    Input Details:
    
    article_structure: This is the predefined outline for the article, including headings, subheadings, and brief descriptions of each section.
     Use this as the main guide for the flow and content of the article.
    context: These are the reference documents that contain relevant information, data, and details necessary to write the article. 
    Ensure you extract key points, facts, and data from these documents to build the content accurately.
    Writing Process:
    
    Step 1: Carefully review the article_structure to understand the flow and requirements of each section.
    Step 2: Analyze the context documents thoroughly, identifying key information that aligns with each part of the article_structure.
    Step 3: Write each section of the article according to the article_structure, integrating relevant information from the context documents. Ensure the writing is coherent, informative, and logically structured.
    Step 4: Use clear, concise language and maintain the tone appropriate for the target audience.
    Using Additional Tools:
    
    If you encounter gaps in information or need further details to enhance the article, you are permitted to use additional tools from the provided list to search the internet for credible sources.
    Ensure any additional information obtained is fact-checked, relevant, and properly integrated into the article.
    Output Requirements:
    
    Deliver the completed article in a well-formatted text, adhering to the provided article_structure.
    Ensure the article is comprehensive, covers all necessary points, and aligns with the original objective of the assignment.
    Include citations or references for any additional information gathered from external sources.
    Final Review:
    
    Proofread the article for grammar, clarity, and consistency.
    Verify that all sections align with the initial article_structure and effectively utilize the information from the context documents.

    
    You have access to the following tools:
    {tools}
    Use the following format:
    Task: the input task you must complete
    Thought: you should always think about what to do
    Action: the action to take should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat 3 times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input task
    
    Begin!
    Article structure: {article_structure}
    Context: {context}
    Thought:{agent_scratchpad}
""")

react_agent_runnable = create_react_agent(llm, tools, react_prompt)
agent_executor = AgentExecutor(agent=react_agent_runnable, tools=tools,verbose=True)

def write_article(state: MainState) -> dict:
    article_structure = state["article_structure"]
    documents = state["search_results"]

    try:
        response = agent_executor.invoke({"article_structure":article_structure, "context":documents })
    except ValueError as e:
        response = str(e)
        if not response.startswith("Could not parse LLM output: `"):
            raise e
        response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
    print(f"Generated article: {response}")

    return {"article": response}
