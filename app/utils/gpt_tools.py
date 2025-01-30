import warnings

from dotenv import load_dotenv, find_dotenv
from langchain.memory import ConversationBufferMemory

from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from sqlalchemy.ext.asyncio import AsyncSession

from app.storage.crud.message_crud import get_history, clean_history, save_message
from app.storage.models.message import MessageType

load_dotenv(find_dotenv())
warnings.filterwarnings("ignore")


# user_memories = {}
llm = ChatOpenAI(model_name="gpt-4o-mini", max_tokens=3000)

template = """
Here's the conversation history: {history}

You are a helpful chatbot. Respond to the user's question: {question}
"""
prompt = PromptTemplate(template=template, input_variables=["history", "question"])


async def get_user_chain(session: AsyncSession,user_id: int):
    history = await get_history(session, user_id)
    history = "\n".join([f"{message.type}: {message.text}" for message in history])

    memory = ConversationBufferMemory(input_key="question", memory_key="history")
    memory.save_context({"question": "start"}, {"history": history})
    return LLMChain(llm=llm, prompt=prompt, memory=memory)


async def process_message(session: AsyncSession, user_id: int, message: str):
    chain = await get_user_chain(session, user_id)

    await save_message(session, user_id, message, MessageType.USER)

    response = await chain.ainvoke({"question": message})
    response_text = response["text"]
    await save_message(session, user_id, response_text, MessageType.ASSISTANT)
    return response_text


async def clear_memory(session: AsyncSession, user_id: int):
    await clean_history(session, user_id)


    # if login in user_memories:
    #     del user_memories[login]
