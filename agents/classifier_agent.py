from crewai import Agent
from tools.classifier_tool import ClassifierTool

def ClassifierAgent(llm):
    return Agent(
        role='Domain Classifier',
        goal='Classify the document domain from a set list (hospital, academic, HR)',
        backstory='You are an expert at categorizing documents by content and rejecting irrelevant ones.',
        tools=[ClassifierTool()],
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
