This is a simple project to use llm agents for lead research. Give the name of the company, and the llm will find the company website and get basic details. 

Steps to implement

1. Clone this repo
2. Install the following libraries in your virtual environment
    a. langchain
    b. openai 
    c. beautifulsoup4 
    d. requests 
    e. google-search-results 
    f. python-dotenv
    g. langchain-community
3. Run python3 llm_browsing.py

In addition you will need the api key from Serp https://serpapi.com/ for google search  and openai API key to interpret the results from the website

You can change the company_name = "Royal Engineering Works" value to get the actual value for 

1. Founded when
2. Geographic locations
3. Products and services

Still blows my mind that it takes a few lines of code and maybe an hour to implement lead research, something that took quite a bit of time and inaccuracies before LLMs came into the scene
