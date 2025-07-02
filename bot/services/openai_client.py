"""OpenAI client for generating location facts."""

import json
import logging

import httpx
from openai import AsyncOpenAI

from config.settings import settings

logger = logging.getLogger(__name__)


class OpenAIClient:
    """Client for interacting with OpenAI API."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=httpx.Timeout(settings.openai_timeout),
        )

    async def get_location_fact(
        self, latitude: float, longitude: float, language: str = "ru"
    ) -> str | None:
        """
        Get an interesting fact about a location.

        Args:
            latitude: Location latitude
            longitude: Location longitude
            language: Language for the response ("ru" or "en")

        Returns:
            Interesting fact about the location or None if error
        """
        try:
            system_prompt = (
                settings.system_prompt_ru
                if language == "ru"
                else settings.system_prompt_en
            )

            user_content = json.dumps({"latitude": latitude, "longitude": longitude})

            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                temperature=settings.openai_temperature,
                max_tokens=settings.openai_max_tokens,
            )

            fact = response.choices[0].message.content

            # Trim to 512 characters if needed
            if fact and len(fact) > 512:
                fact = fact[:509] + "..."

            return fact

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return None


# Create singleton instance
openai_client = OpenAIClient()
