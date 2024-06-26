import os
from dotenv import load_dotenv
import re
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.utilities import SerpAPIWrapper

load_dotenv()

# Set your API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

# Initialize the language model
llm = OpenAI(temperature=0)

# Initialize SerpAPIWrapper
search = SerpAPIWrapper()

# Load the necessary tools
tools = load_tools(["serpapi"], llm=llm, serpapi_api_key=os.environ["SERPAPI_API_KEY"])

# Initialize the agent
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

def search_company_website(company_name):
    # Use the agent to search for the company website
    result = agent.run(f"Find the official website URL for {company_name}. Only return the URL.")
    
    # Extract URL from the result using regex
    url_match = re.search(r'https?://\S+', result)
    if url_match:
        return url_match.group(0)
    else:
        raise ValueError(f"No valid URL found in the result: {result}")

def scrape_company_info(url):
    # Load the web page content
    loader = WebBaseLoader(url)
    document = loader.load()
    
    # Create a prompt template
    prompt_template = PromptTemplate(
        input_variables=["page_content"],
        template="""
        Based on the following webpage content, please extract and summarize the following information about the company:
        1. When the company was founded
        2. The company's main products and services
        3. The geographic locations where the company operates

        If any information is not explicitly stated, indicate that it's not found.

        Webpage content:
        {page_content}

        Summary:
        """
    )

    # Create an LLMChain
    chain = LLMChain(llm=llm, prompt=prompt_template)

    # Run the chain
    result = chain.run(page_content=document[0].page_content)

    return result

# Example usage
company_name = "Royal Engineering Works"
try:
    website = search_company_website(company_name)
    print(f"Company: {company_name}")
    print(f"Website: {website}")
    
    company_info = scrape_company_info(website)
    print("Company Information:")
    print(company_info)
except Exception as e:
    print(f"An error occurred: {str(e)}")
