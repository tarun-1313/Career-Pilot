"""
Gemini AI Client for CareerPilot AI
Handles all interactions with Google Gemini API.
Replaces the emergentintegrations.llm.chat dependency.
"""

import os
import json
import logging
from typing import Optional, List, Dict, Any, AsyncGenerator
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

# Configure logging
logger = logging.getLogger("careerpilot.gemini")

# Constants
GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 8192


class GeminiError(Exception):
    """Custom exception for Gemini API errors."""
    pass


class GeminiClient:
    """Async client for Google Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Gemini API key. If not provided, will use GEMINI_API_KEY env var.
        
        Raises:
            GeminiError: If no API key is available.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise GeminiError(
                "Gemini API key not found. Set GEMINI_API_KEY in environment variables."
            )
        
        try:
            self.client = genai.Client(api_key=self.api_key)
            logger.info("Gemini client initialized successfully")
        except Exception as e:
            raise GeminiError(f"Failed to initialize Gemini client: {e}")
    
    async def generate_text(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: The user prompt.
            system_message: Optional system message for context.
            temperature: Sampling temperature (0-2).
            max_tokens: Maximum tokens to generate.
        
        Returns:
            Generated text string.
        
        Raises:
            GeminiError: If generation fails.
        """
        try:
            contents = []
            if system_message:
                contents.append(types.Content(
                    role="model",
                    parts=[types.Part(text=system_message)]
                ))
            
            contents.append(types.Content(
                role="user",
                parts=[types.Part(text=prompt)]
            ))
            
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            response = await self.client.aio.models.generate_content(
                model=GEMINI_MODEL,
                contents=contents,
                config=config,
            )
            
            return response.text or ""
            
        except Exception as e:
            logger.error(f"Text generation failed: {e}")
            raise GeminiError(f"Text generation failed: {e}")
    
    async def generate_json(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> Dict[str, Any]:
        """
        Generate JSON from a prompt.
        
        Args:
            prompt: The user prompt.
            system_message: Optional system message for context.
            temperature: Sampling temperature.
        
        Returns:
            Parsed JSON dictionary.
        
        Raises:
            GeminiError: If generation or parsing fails.
        """
        try:
            json_prompt = prompt + "\n\nIMPORTANT: Return ONLY valid JSON with double quotes, no single quotes, no markdown, no code fences."
            
            response = await self.generate_text(
                prompt=json_prompt,
                system_message=system_message,
                temperature=temperature,
                max_tokens=DEFAULT_MAX_TOKENS,
            )
            
            # Clean up the response
            text = response.strip()
            
            # Remove markdown code fences if present
            if text.startswith("```"):
                lines = text.split("\n")
                if lines[0].lower().startswith("```json"):
                    lines = lines[1:]
                elif lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                text = "\n".join(lines).strip()
            
            # Try to fix single quotes to double quotes
            import re
            text = re.sub(r"'([^']+)'", r'"\1"', text)
            
            # Find JSON boundaries
            start_idx = text.find("{")
            end_idx = text.rfind("}")
            
            if start_idx >= 0 and end_idx > start_idx:
                text = text[start_idx:end_idx + 1]
            
            # Try parsing JSON, if failed try some more fixes
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                # Try to fix common issues: unescaped newlines in strings, etc.
                import ast
                try:
                    return ast.literal_eval(text)
                except Exception:
                    logger.error(f"All JSON parsing attempts failed. Raw text: {response[:800]}")
                    raise
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}. Raw text: {response[:500]}")
            raise GeminiError(f"Failed to parse JSON response: {e}")
        except Exception as e:
            logger.error(f"JSON generation failed: {e}")
            raise GeminiError(f"JSON generation failed: {e}")
    
    async def stream_text(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> AsyncGenerator[str, None]:
        """
        Stream text generation.
        
        Args:
            prompt: The user prompt.
            system_message: Optional system message.
            temperature: Sampling temperature.
        
        Yields:
            Text chunks as they are generated.
        """
        try:
            # Prepare messages
            messages = []
            if system_message:
                messages.append(types.Content(
                    role="model",
                    parts=[types.Part(text=system_message)]
                ))
            messages.append(types.Content(
                role="user",
                parts=[types.Part(text=prompt)]
            ))
            
            config = types.GenerateContentConfig(
                temperature=temperature,
            )
            
            # For now, use synchronous generation and yield the whole text at once
            # This will be non-streaming, but it will at least work!
            response = await self.client.aio.models.generate_content(
                model=GEMINI_MODEL,
                contents=messages,
                config=config,
            )
            
            if response.text:
                yield response.text
                    
        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            raise GeminiError(f"Streaming failed: {e}")


# Global client instance
_gemini_client: Optional[GeminiClient] = None


def get_gemini_client() -> GeminiClient:
    """Get or create the global Gemini client instance."""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client


def reset_gemini_client():
    """Reset the global client (useful for testing)."""
    global _gemini_client
    _gemini_client = None


# Convenience functions for direct use
async def gemini_generate_text(
    prompt: str,
    system_message: Optional[str] = None,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> str:
    """Generate text using Gemini."""
    client = get_gemini_client()
    return await client.generate_text(prompt, system_message, temperature, max_tokens)


async def gemini_generate_json(
    prompt: str,
    system_message: Optional[str] = None,
    temperature: float = DEFAULT_TEMPERATURE,
) -> Dict[str, Any]:
    """Generate JSON using Gemini."""
    client = get_gemini_client()
    return await client.generate_json(prompt, system_message, temperature)


async def gemini_stream_text(
    prompt: str,
    system_message: Optional[str] = None,
    temperature: float = DEFAULT_TEMPERATURE,
) -> AsyncGenerator[str, None]:
    """Stream text using Gemini."""
    client = get_gemini_client()
    async for chunk in client.stream_text(prompt, system_message, temperature):
        yield chunk
