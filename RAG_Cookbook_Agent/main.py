from crewai import Agent, Task, Crew, LLM
from tools.rag_solution_tool import RAGSolutionTool
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# RAG tool
rag_tool = RAGSolutionTool()

# Gemini LLM for the agent
llm = LLM(
    model="gemini/gemini-2.0-flash",
    provider="google",
    api_key=GEMINI_API_KEY
)

# Agent
error_agent = Agent(
    role="CI/CD Troubleshooter",
    goal="Resolve error logs using semantic search and LLM",
    backstory="A smart agent that uses retrieval-augmented generation to fix pipeline errors.",
    tools=[rag_tool],
    llm=llm,
    verbose=True
)

# Sample task
error_msg = "ERROR: Docker build failed"

task = Task(
    description=f"Resolve this error: {error_msg}",
    expected_output="Clear and actionable resolution.",
    agent=error_agent
)

crew = Crew(agents=[error_agent], tasks=[task], verbose=True)
result = crew.kickoff()
print("💡 Final Output:\n", result)
