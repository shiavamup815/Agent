from crewai import Agent
from tools.email_tool import EmailSenderTool

def EmailAgent(llm):
    return Agent(
        role='Email Sender',
        goal='Send the formatted summary via email',
        backstory='Knows how to draft and send professional emails',
        tools=[EmailSenderTool()],
        verbose=True,
        llm=llm
    )
