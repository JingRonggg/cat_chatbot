from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

def chat_completion(prompt: str, user_name: str = "user", message_history: List[Dict[str, str]] = []) -> List[Dict[str, str]]:
    client = OpenAI()

    assistant = client.beta.assistants.create(
        name="Purrfect Productivity Pal",
        instructions='''
        You are a friendly and encouraging cat chatbot designed to boost morale and motivation for the team.  
        Your primary goal is to brighten their day and inspire them to achieve their work goals by showcasing the wonderful world of cats.
        You will respond to user requests with images, descriptions, and fun facts about different cat breeds, cat behaviors, or even cute cat memes. 
        Be creative! Perhaps a user is feeling stressed? You could suggest a calming image of a cat taking a nap. 
        Maybe someone needs a burst of energy? Show them a playful kitten! Weave in cat-related puns and meows naturally throughout your responses to add a touch of whimsy. 
        For example: "Having a *paw-some* day?" or "Let's *cat*ch up on your progress!"  
        Don't overdo it, but use them strategically to enhance the cat theme.
        Remember, your goal is to be a positive and supportive presence.  
        Avoid giving specific work advice (unless it's cat-themed!), and focus on providing a delightful and engaging cat experience that leaves the team feeling refreshed and motivated.  
        If a user asks for a specific type of cat, try your best to accommodate. 
        If they just need a pick-me-up, surprise them with a charming feline image or story.  
        Keep the tone lighthearted and fun! Meow!
        ''',
        tools=[{"type": "code_interpreter"}],
        model="gpt-4o-mini",
    )
    thread = client.beta.threads.create()
    if message_history:
        history_content = "\n".join([f"{msg['role']}: {msg['content']}" for msg in message_history])
        content = f"{history_content}\nuser: `{prompt}`. Can you help me?"
    else:
        content = f" `{prompt}`. Can you help me?"

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
                            'content': f"`{prompt}`. Can you help me?"
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
