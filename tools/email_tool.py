from crewai.tools import BaseTool
from pydantic import Field
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()  

class EmailSenderTool(BaseTool):
    name: str = Field(default="EmailSender", description="Tool to send the formatted content to the stakeholder.")
    description: str = Field(default="Sends an actual email with the formatted summary content.")

    def _run(self, content: str) -> str:
        
        sender_email = os.getenv("GMAIL_USER")
        sender_password = os.getenv("GMAIL_PASSWORD")
        recipient_email = os.getenv("GMAIL_RECIPIENT", "recipient@example.com") 

        
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = "Task Output - Automated Summary"

        body = f"""
        Dear Stakeholder,

        Please find the completed task below:

        -------------------------------
        {content}
        -------------------------------

        Regards,
        Autonomous Agent
        """

        msg.attach(MIMEText(body, "plain"))

        
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            return f" Real email sent successfully to {recipient_email}."
        except Exception as e:
            return f" Failed to send email. Error: {str(e)}"
