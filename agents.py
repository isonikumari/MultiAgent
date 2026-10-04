from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,scrape_url
load_dotenv()

llm=ChatGoogleGenerativeAI(model="gemini-3.6-flash",temperature=1)
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]

    )
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )

writer_prompts=ChatPromptTemplate.from_messages([
    ("system","You are an expert research Writter.Write clear,structured and insightful reports." ),
    ("human","""Wtite a detailed research report on the topic below.
Topic:{topic}
Research Gathered:{research}

stuctured the output as :
-Intruction
-Key-Findings(minimum 3 well explianed points)
-Conclusion
-sources (list all urls found in research)
Be detailed,factual and professional.
    """)
])

writer_chain=writer_prompts | llm |StrOutputParser()

critic_prompts=ChatPromptTemplate.from_messages([
    ("system","You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the reserch report below and evalute it strictly.

Report:{report}
Response in this exact format:
Score:x/10
Strengths:
- ...
- ...

Areas to improve:
- ...
-...

One line verdict:
...
"""),
])

critic_chain=critic_prompts |llm | StrOutputParser()