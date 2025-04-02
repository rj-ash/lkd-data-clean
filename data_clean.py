from typing import List, Dict
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Load environment variables (only once)
load_dotenv()

# Define Pydantic class for structured output
class LeadDetail(BaseModel):
    name: str = Field(description="Name of the lead")
    bio: str = Field(description="Bio of the lead in a cleaned manner")
    skills: list[str] = Field(description="List of skills")
    experience: str = Field(description="Comprehensive experience in the current company (ignore previous companies)")
    education: str = Field(description="Chronologically ordered education details")

# Ensure API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is missing in environment variables. Set it in your .env file.")

# Initialize LLM Model
model = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=api_key,
    temperature=0.7,
    max_tokens=2048,
)

# Function to clean LinkedIn profile data
def parse_lkd_profile(profile: dict) -> dict:
    if not isinstance(profile, dict):
        raise ValueError("Invalid input: Expected a dictionary.")

    prompt = f"""
    Instruction: Clean and structure the following LinkedIn profile data. Keep the name, skills, curr_company_lkd, and curr_company_url exactly as they are. Clean and format the bio, experience, and education sections. For education, list them chronologically with the most recent first.
    Input: Input is a dictionary in triple-backticks ```{profile}```
    """

    # Use structured output format
    str_model = model.with_structured_output(LeadDetail)

    # Get response from LLM
    result = str_model.invoke(prompt)

    return result.dict()





