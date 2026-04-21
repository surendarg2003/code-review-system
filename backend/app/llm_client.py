import json
import re
from typing import Dict, Any, AsyncGenerator
from groq import AsyncGroq
from .config import settings
from .prompts import CODE_REVIEW_SYSTEM_PROMPT

# Initialize async Groq client
client = AsyncGroq(api_key=settings.GROQ_API_KEY)

async def review_code(code: str, language: str) -> Dict[str, Any]:
    """Send code to Groq LLM and return structured JSON review."""
    prompt = f"Language: {language}\n\nCode:\n{code}"
    try:
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": CODE_REVIEW_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        if not content:
            return {"error": "Empty response from LLM"}
        
        # Robust JSON extraction (handles markdown wrappers or extra text)
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return {"error": "Failed to parse LLM response as valid JSON"}
            
    except Exception as e:
        return {"error": f"LLM request failed: {str(e)}"}

async def review_code_stream(code: str, language: str) -> AsyncGenerator[str, None]:
    """Stream tokens from Groq LLM for real-time output."""
    prompt = f"Language: {language}\n\nCode:\n{code}"
    try:
        stream = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": CODE_REVIEW_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            stream=True,
            response_format={"type": "json_object"}
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield json.dumps({"error": f"Streaming failed: {str(e)}"})