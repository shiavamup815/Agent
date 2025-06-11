from crewai import Agent

def TaskPlannerAgent(llm):
    return Agent(
        role='Task Planner',
        goal='Understand the user goal and create a task plan',
        backstory='You are skilled in decomposing high-level goals into actionable steps.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
