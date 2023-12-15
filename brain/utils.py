from openai import OpenAI
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import os
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from huggingface_hub import InferenceClient
import warnings
warnings.filterwarnings(action='ignore')

os.environ['OPENAI_API_KEY'] = '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'
os.environ['HUGGINGFACEHUB_API_TOKEN'] = "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"

def ask_llm(text, openai_model_name='gpt-3.5-turbo', huggingface_repo_id='google/flan-t5-large', channel='openai'):
    if channel == 'openai':
        llm = OpenAI(temperature=0.6, openai_api_key=os.environ['OPENAI_API_KEY'])
        chatllm = ChatOpenAI(temperature=0.6, openai_api_key=os.environ['OPENAI_API_KEY'], model=openai_model_name)
        response = chatllm([
            SystemMessage(content='You are a medicine and health consultant AI assistant'),
            HumanMessage(content=text)
            ])
        response = str(response)
    else:
        # llm = HuggingFaceHub(repo_id=huggingface_repo_id, model_kwargs={'temperature':0, 'max_length':64})
        # response = llm.predict(text)

        template = """Question: {text} 
        Answer: Let's think step by step."""
        prompt = PromptTemplate(template=template, input_variables=["question"])

        huggingface_repo_id = "google/flan-t5-xxl"

        llm = HuggingFaceHub(
            repo_id=huggingface_repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
            )
        llm_chain = LLMChain(prompt=prompt, llm=llm)

        response = llm_chain.run(text)
    return response

if __name__ == '__main__':
    # text = 'I have vitamin b12 deficiency. What should I do?'
    text = 'what is 2+2'
    print(ask_llm(text=text, channel='openai'))