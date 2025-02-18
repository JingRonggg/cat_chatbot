from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

def chat_completion(topic: str, user_name: str = "user", message_history: List = []) -> List:
    client = OpenAI()

    assistant = client.beta.assistants.create(
        name="Financial Motivator",
        instructions='''
        You are a personal financial motivator. 
        Your goal is to inspire and encourage the user to learn about finance. 
        You will provide positive reinforcement, suggest learning resources, 
        break down complex topics into digestible chunks, and celebrate their progress.  
        You can also provide practical exercises and challenges to help them apply their knowledge.  
        Avoid giving specific financial advice, instead guide them towards learning the underlying principles and 
        encourage them to consult with qualified professionals for personalised guidance.
        Meow at the correct places in the conversation. 
        Put in subtle meows as puns or jokes.
        ''',
        tools=[{"type": "code_interpreter"}],
        model="gpt-4o-mini",
    )

    thread = client.beta.threads.create()

    if message_history:
        history_content = "\n".join([f"{msg['role']}: {msg['content']}" for msg in message_history])
        content = f"{history_content}\nuser: I need help with this concept `{topic}`. Can you help me?"
    else:
        content = f"user: I need help with this concept `{topic}`. Can you help me?"

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=f"Please address the user as {user_name}. The user has a premium account."
    )

    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        
        for msg in messages:
            if msg.role == 'user':
                for content_block in msg.content:
                    if content_block.type == 'text':
                        message_history.append({
                            'role': msg.role,
                            'content': f"I need help with this concept `{topic}`. Can you help me?"
                        })
            if msg.role == 'assistant':
                for content_block in msg.content:
                    if content_block.type == 'text':
                        message_history.append({
                            'role': msg.role,
                            'content': content_block.text.value
                            })
        return message_history
    else:
        return run.status
