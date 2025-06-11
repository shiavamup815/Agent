from crewai import Agent
from tools.summarizer_tool import SummarizerTool

def SummarizerAgent(llm):
    return Agent(
        role='Summarizer',
        goal='Summarize the provided content effectively',
        backstory='Expert in concise document summarization',
        tools=[SummarizerTool()],
        verbose=True,
        llm=llm
    )
