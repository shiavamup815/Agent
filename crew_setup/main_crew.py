# from crewai import Crew, LLM#, CrewMemory
# from agents.task_planner_agent import TaskPlannerAgent
# from agents.summarizer_agent import SummarizerAgent
# from agents.formatter_agent import FormatterAgent
# from agents.email_agent import EmailAgent

# llm = LLM(
#     model="gemini/gemini-2.0-flash",
#     provider="google"
# )

# #memory = CrewMemory()

# def run_crew(user_goal):
#     planner = TaskPlannerAgent(llm)
#     summarizer = SummarizerAgent(llm)
#     formatter = FormatterAgent(llm)
#     emailer = EmailAgent(llm)

#     crew = Crew(
#         agents=[planner, summarizer, formatter, emailer],
#         #agents=[planner, summarizer, formatter],
#         tasks=[
#             {
#                 "agent": planner,
#                 "description": f"Understand and plan the goal: {user_goal}",
#                 "expected_output": "A list of actionable sub-tasks derived from the goal."
#             },
#             {
#                 "agent": summarizer,
#                 "description": "Summarize the document",
#                 "expected_output": "A concise summary of the input document."
#             },
#             {
#                 "agent": formatter,
#                 "description": "Format the summary",
#                 "expected_output": "A markdown-formatted summary suitable for sending via email."
#             },
#             {
#                 "agent": emailer,
#                 "description": "Send the formatted summary",
#                 "expected_output": "A confirmation that the email was sent successfully."
#             }
#         ],
#         #memory= True,
#         verbose=True
#     )
#     crew.kickoff()



# from crewai import Crew, LLM
# from agents.task_planner_agent import TaskPlannerAgent
# from agents.summarizer_agent import SummarizerAgent
# from agents.formatter_agent import FormatterAgent
# from agents.email_agent import EmailAgent
# from agents.classifier_agent import ClassifierAgent

# llm = LLM(
#     model="gemini/gemini-2.0-flash",
#     provider="google"
# )

# # Global to pass classification result
# classified_domain = None

# def run_crew(user_goal) -> str:
#     global classified_domain

#     planner = TaskPlannerAgent(llm)
#     summarizer = SummarizerAgent(llm)
#     classifier = ClassifierAgent(llm)
#     formatter = FormatterAgent(llm)
#     emailer = EmailAgent(llm)

#     crew = Crew(
#         agents=[planner, summarizer, classifier, formatter, emailer],
#         tasks=[
#             {
#                 "agent": planner,
#                 "description": f"Understand and plan the goal: {user_goal}",
#                 "expected_output": "A list of actionable sub-tasks derived from the goal."
#             },
#             {
#                 "agent": summarizer,
#                 "description": "Summarize the document",
#                 "expected_output": "A concise summary of the input document."
#             },
#             {
#                 "agent": classifier,
#                 "description": "Classify the document's domain from hospital, academic, or HR.",
#                 "expected_output": "One of the following: hospital, academic, HR, or unknown."
#             }
#         ],
#         verbose=True
#     )

#     results = crew.kickoff()
    
#     # Check the classifier's output
#     #domain = results[-1].strip().lower()


#     domain = results.raw.lower()



#     classified_domain = domain

#     if domain not in ["hospital", "academic", "hr"]:
#         return f" Document domain '{domain}' is not supported. Workflow stopped."
    
#     # If valid domain, continue remaining agents manually
#     crew = Crew(
#         agents=[formatter, emailer],
#         tasks=[
#             {
#                 "agent": formatter,
#                 "description": "Format the summary",
#                 "expected_output": "A markdown-formatted summary suitable for sending via email."
#             },
#             {
#                 "agent": emailer,
#                 "description": "Send the formatted summary",
#                 "expected_output": "A confirmation that the email was sent successfully."
#             }
#         ],
#         verbose=True
#     )
    
#     crew.kickoff()
#     return f" Document classified as '{domain}' and workflow completed."

from crewai import Crew, LLM
from agents.task_planner_agent import TaskPlannerAgent
from agents.summarizer_agent import SummarizerAgent
from agents.formatter_agent import FormatterAgent
from agents.email_agent import EmailAgent
from agents.classifier_agent import ClassifierAgent

llm = LLM(
    model="gemini/gemini-2.0-flash",
    provider="google"
)

def run_crew(user_goal) -> str:
    # Initialize agents
    planner = TaskPlannerAgent(llm)
    summarizer = SummarizerAgent(llm)
    classifier = ClassifierAgent(llm)
    formatter = FormatterAgent(llm)
    emailer = EmailAgent(llm)

    # Phase 1: plan → summarize → classify
    crew1 = Crew(
        agents=[planner, summarizer, classifier],
        tasks=[
            {
                "agent": planner,
                "description": f"Understand and plan the goal: {user_goal}",
                "expected_output": "A list of actionable sub-tasks derived from the goal."
            },
            {
                "agent": summarizer,
                "description": "Summarize the document",
                "expected_output": "A concise summary of the input document."
            },
            {
                "agent": classifier,
                "description": "Classify the document's domain from hospital, academic, or HR.",
                "expected_output": "One of the following: hospital, academic, HR, or unknown."
            }
        ],
        #memory=True,  # ✅ enable memory using flag
        verbose=True
    )

    results1 = crew1.kickoff()

    #domain_output = results1[2].raw_output.strip().lower()


    domain_output = results1[2].strip().lower()

    if domain_output not in ["hospital", "academic", "hr"]:
        return f"🚫 Document domain '{domain_output}' is not supported. Workflow stopped."

    # Phase 2: format → email (uses memory from phase 1)
    crew2 = Crew(
        agents=[formatter, emailer],
        tasks=[
            {
                "agent": formatter,
                "description": "Format the summary",
                "expected_output": "A markdown-formatted summary suitable for sending via email."
            },
            {
                "agent": emailer,
                "description": "Send the formatted summary",
                "expected_output": "A confirmation that the email was sent successfully."
            }
        ],
        #memory=True,  # ✅ re-enable memory here
        verbose=True
    )

    crew2.kickoff()

    return f"✅ Document classified as '{domain_output}' and workflow completed."
