import os
from crewai import Agent, Task
from crewai_tools import ScrapeWebsiteTool, FileWriterTool
from TEXT_TOOLS.summarize import SummarizationTool  # ✅ your summarization tool
from TEXT_TOOLS.change_persona import ChangePersonaTool
from TEXT_TOOLS.doc_classify import DocumentClassificationTool  # ✅ your classifier tool
from langchain_groq import ChatGroq
# Set environment variables
os.environ['GROQ_API_KEY'] = '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'
os.environ['GROQ_MODEL'] = 'groq/llama-3.1-8b-instant'  # correct model name
os.environ['OPENAI_API_KEY'] = 'sk-svcacct-A7-TCvp0gxsoY3tYlyYylhkSXfMhxlcf9Th10nZ97KN-3_Aeg09dfok1f-5rXp-HsT3BlbkFJhVGr7-SGP31NP9uACoI6s16yfT9q20sPBPqRxdb47C0S04KqdD-gkwAeZy19h8rAA'  # for any openai integration if needed


from dotenv import load_dotenv
# Load environment variables
load_dotenv()
# Load LLM (optional for summarization or persona tools if they require it)
groq_llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="groq/llama-3.1-8b-instant",
    temperature=0.2,
    max_tokens=2000
)
print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))  # Debugging line to check if the key is set
summarisation_tool = SummarizationTool()
change_persona_tool= ChangePersonaTool()
document_classification_tool = DocumentClassificationTool()
scraper_tool = ScrapeWebsiteTool()



# Agents
scraper_agent = Agent(
    role="Web Scraper",
    goal="Extract textual content from websites",
    backstory="Expert at scraping meaningful article content from web pages.",
    tools=[scraper_tool],
    verbose=True
)

summarizer_agent = Agent(
    role="Summarizer",
    goal="Summarize lengthy articles into less than 2000 words concise form",
    backstory="Distills articles into digestible and accurate summaries.",
    tools=[summarisation_tool],
    verbose=True
)

persona_agent = Agent(
    role="Persona Stylist",
    goal="Rewrite text in a specific style or persona",
    backstory="Adapts any text to sound like a particular persona, author, or tone.",
    tools=[change_persona_tool],
    verbose=True
)

classifier_agent = Agent(
    role="Document Classifier",
    goal="Classify document category or domain",
    backstory="Understands and classifies text into categories like technical, educational, legal, etc.",
    tools=[document_classification_tool],
    verbose=True
)



# URL to process
website_url = "https://medium.com/@shraddharao_/brute-force-technique-in-algorithms-34bac04bde8a"

# 1. Scrape text
print("\n🔍 Scraping website...")
scrape_task = Task(
    description=f"Scrape the article content from this URL: {website_url}",
    expected_output="Clean article text",
    agent=scraper_agent
)
scraped_text = scraper_agent.execute_task(scrape_task)

# 2. Summarize
print("\n🧠 Summarizing content...")
summary_task = Task(
    description=f"Summarize the following article:\n\n{scraped_text}",
    expected_output="Concise summary",
    agent=summarizer_agent
)
summary_text = summarizer_agent.execute_task(summary_task)

# 3. Apply persona
print("\n🎭 Applying persona transformation...")
persona_task = Task(
    description=f"Rewrite the following text in the persona of an IIT CSE Professor:\n\n{scraped_text}",
    expected_output="Text rewritten in target persona style",
    agent=persona_agent
)
persona_text = persona_agent.execute_task(persona_task)

# 4. Classify document
print("\n🧾 Classifying document type...")
classify_task = Task(
    description=f"Classify the topic or category of the following article:\n\n{scraped_text}",
    expected_output="Category label (e.g., education, technical, opinion, news)",
    agent=classifier_agent
)
classification = classifier_agent.execute_task(classify_task)

# 5. Write final report
print("\n📝 Generating final report...")
# ✅ Define the FileWriterTool to save in .txt format
reporting_tool = FileWriterTool(file_path='workflow2_report.txt')

# ✅ Create the reporting agent
reporting_agent = Agent(
    role="Markdown Reporter",
    goal="Generate final report in plain text format and save it",
    backstory="Creates structured and readable final reports summarizing all outputs.",
    tools=[reporting_tool],
    verbose=True
)

# ✅ Define the report writing task
report_task = Task(
    description=f"""Write a plain text report that includes:
1. Summary of the article: {summary_text}
2. Persona-styled version: {persona_text}
3. Document classification: {classification}

Format it with clear sections and titles.
""",
    expected_output="A text file 'final_report.txt' saved in the current directory.",
    agent=reporting_agent,
    output_file='workflow2_report.txt'  # Ensures CrewAI routes output to this file
)

# ✅ Execute the final task
report_result = reporting_agent.execute_task(report_task)

# ✅ Done
print("\n✅ DONE! Final report written to 'workflow2_report.txt'.")
print(report_result)
