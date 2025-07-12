from g4f.client import Client
import logging
import asyncio
import time

"""YOU CAN ALSO IMPORT YOUR PROVIDER HERE"""
from config.settings import prompt, model, client, max_retries, retry_delay 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIResponseError(Exception):
    pass

async def create_response(
    text: str,
    prompt: str = prompt,
    client: str = client,
    model: str = model,
    max_retries: int = max_retries,
    retry_delay: float = retry_delay
) -> str:
    if not text.strip():
        raise ValueError("The text cant be empty")
    
    g4f_client = Client() if client == "g4f" else None # YOU CAN ADD PROVIDER: Client(provider=YOUR PROVIDER)
    
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text}
    ]
    
    last_error = None
    start_time = time.time()
    
    for attempt in range(max_retries):
        try:
            response = g4f_client.chat.completions.create(
                    model=model,
                    messages=messages
            )

            if not response.choices:
                raise AIResponseError("Empty text from ai")
                 
            return response.choices[0].message.content
            
        except Exception as e:
            last_error = e
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay * (attempt + 1))

        finally:
            elapsed_time = time.time() - start_time
            logging.info(f'The response from model was successfully send: {round(elapsed_time, 2)} sec')
    
    raise AIResponseError(f"Failed to catch response for {max_retries} retryes. Last fail: {str(last_error)}")
