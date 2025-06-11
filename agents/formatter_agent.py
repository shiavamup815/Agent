from crewai import Agent
from tools.formatter_tool import FormatterTool

def FormatterAgent(llm):
    return Agent(
        role='Formatter',
        goal='Format content into markdown or styled format',
        backstory='Skilled in content formatting and markdown styling',
        tools=[FormatterTool()],
        verbose=True,
        llm=llm
    )
