from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
import requests
import os

load_dotenv()

CAT_API_KEY = os.getenv("CAT_API_KEY")

def get_cat_image(limit: int = 1) -> List[str]:
    """
    Fetches cat images from The Cat API.
    
    Args:
        limit (int, optional): The number of cat images to fetch. Defaults to 1.
    
    Returns:
        List[str]: A list of URLs pointing to cat images.
    """
    url = "https://api.thecatapi.com/v1/images/search"
    headers = {
        "x-api-key": CAT_API_KEY
    }
    params = {
        "limit": limit
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return [cat["url"] for cat in data]

def chat_completion(prompt: str, user_name: str = "user") -> List[Dict[str, str]]:
    """
    Generates a chat response using OpenAI's GPT model with a cat-themed assistant.
    
    Args:
        prompt (str): The user's input message.
        user_name (str, optional): The name to address the user. Defaults to "user".
    
    Returns:
        List[Dict[str, str]]: A list of messages from the assistant, including text responses and cat images if applicable.
    """
    client = OpenAI()

    tool = [
    {
        "type": "function",
        "function": {
            "name": "get_cat_image",
            "description": "Get different pictures of cats from The Cat API",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer"}
                },
                "required": ["limit"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "code_interpreter"
    }
    ]

    ## Assistant creation
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
        tools=tool,
        model="gpt-4o-mini",
    )
    thread = client.beta.threads.create()
    content = f" `{prompt}`. Can you help me?"

    ### Create a message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
    )

    print(f"this is message: {message}")

    try:
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions=f"Please address the user as {user_name}. The user has a premium account."
        )
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            return [{
                'role': 'assistant',
                'content': "Could you repeat yourself?"
            }]
        else:
            raise e

    if run.status == 'requires_action':
        tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
        tool_output = get_cat_image(limit=1)[0]
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=[{
                "tool_call_id": tool_call.id,
                "output": tool_output
            }]
        )
        run = client.beta.threads.runs.poll(thread_id=thread.id, run_id=run.id)

    print(f"this is run: {run}")
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        message_history = []
        for msg in messages:
            if msg.role == 'assistant':
                for content_block in msg.content:
                    if content_block.type == 'text':
                        message_history.append({
                            'role': msg.role,
                            'content': content_block.text.value
                            })
        return message_history
    else:
        return [{'role': 'assistant', 'content': run.status}]