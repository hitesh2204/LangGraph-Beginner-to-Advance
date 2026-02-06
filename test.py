from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
import os

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    temperature=0.7,
    max_new_tokens=100
)

prompt = PromptTemplate(
        template='Create congratulations message for {name}',
        input_variables=['name']
    )
response = prompt.invoke({'name':"Sannidhya"})
print(response)

output =llm.invoke(response)
print(output)