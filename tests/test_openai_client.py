"""Tests for OpenAI client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from bot.services.openai_client import OpenAIClient


@pytest.fixture
def openai_client():
    """Create OpenAI client instance for testing."""
    with patch("bot.services.openai_client.settings") as mock_settings:
        mock_settings.openai_api_key = "test-key"
        mock_settings.openai_timeout = 30
        mock_settings.openai_model = "gpt-4o-mini"
        mock_settings.openai_temperature = 1.0
        mock_settings.openai_max_tokens = 200
        mock_settings.system_prompt_ru = "Test prompt RU"
        mock_settings.system_prompt_en = "Test prompt EN"

        client = OpenAIClient()
        return client


@pytest.mark.asyncio
async def test_get_location_fact_success(openai_client):
    """Test successful fact generation."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = (
        "This is an interesting fact about the location."
    )

    with patch.object(
        openai_client.client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = mock_response

        fact = await openai_client.get_location_fact(55.7558, 37.6173)

        assert fact == "This is an interesting fact about the location."
        mock_create.assert_called_once()

        # Check call arguments
        call_args = mock_create.call_args[1]
        assert call_args["model"] == "gpt-4o-mini"
        assert call_args["temperature"] == 1.0
        assert call_args["max_tokens"] == 200


@pytest.mark.asyncio
async def test_get_location_fact_truncate_long_response(openai_client):
    """Test that long responses are truncated to 512 characters."""
    long_fact = "A" * 600  # Create a 600-character string

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = long_fact

    with patch.object(
        openai_client.client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = mock_response

        fact = await openai_client.get_location_fact(55.7558, 37.6173)

        assert len(fact) == 512
        assert fact.endswith("...")
        assert fact[:509] == "A" * 509


@pytest.mark.asyncio
async def test_get_location_fact_error_handling(openai_client):
    """Test error handling when API call fails."""
    with patch.object(
        openai_client.client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.side_effect = Exception("API Error")

        fact = await openai_client.get_location_fact(55.7558, 37.6173)

        assert fact is None


@pytest.mark.asyncio
async def test_get_location_fact_language_selection(openai_client):
    """Test that correct system prompt is selected based on language."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Fact"

    with patch.object(
        openai_client.client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = mock_response

        # Test Russian
        await openai_client.get_location_fact(55.7558, 37.6173, language="ru")
        call_args = mock_create.call_args[1]
        assert call_args["messages"][0]["content"] == "Test prompt RU"

        # Test English
        await openai_client.get_location_fact(55.7558, 37.6173, language="en")
        call_args = mock_create.call_args[1]
        assert call_args["messages"][0]["content"] == "Test prompt EN"
