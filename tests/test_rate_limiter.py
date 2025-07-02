"""Tests for rate limiter service."""

import asyncio
from unittest.mock import patch

import pytest

from bot.services.rate_limiter import RateLimiter


@pytest.fixture
def rate_limiter():
    """Create rate limiter instance for testing."""
    with patch("bot.services.rate_limiter.settings") as mock_settings:
        mock_settings.rate_limit_requests = 1
        mock_settings.rate_limit_period = 5

        limiter = RateLimiter()
        return limiter


@pytest.mark.asyncio
async def test_rate_limit_allows_first_request(rate_limiter):
    """Test that first request is allowed."""
    user_id = 12345

    # First request should be allowed
    can_proceed = await rate_limiter.check_rate_limit(user_id)
    assert can_proceed is True


@pytest.mark.asyncio
async def test_rate_limit_blocks_rapid_requests(rate_limiter):
    """Test that rapid requests are blocked."""
    user_id = 12345

    # First request
    can_proceed = await rate_limiter.check_rate_limit(user_id)
    assert can_proceed is True
    await rate_limiter.acquire(user_id)

    # Second immediate request should be blocked
    can_proceed = await rate_limiter.check_rate_limit(user_id)
    assert can_proceed is False


@pytest.mark.asyncio
async def test_rate_limit_allows_after_period(rate_limiter):
    """Test that requests are allowed after rate limit period."""
    user_id = 12345

    # Mock the rate limiter to have a very short period for testing
    rate_limiter.time_period = 0.1  # 100ms
    rate_limiter.limiters.clear()  # Clear any existing limiters

    # First request
    can_proceed = await rate_limiter.check_rate_limit(user_id)
    assert can_proceed is True
    await rate_limiter.acquire(user_id)

    # Should be blocked immediately
    can_proceed = await rate_limiter.check_rate_limit(user_id)
    assert can_proceed is False

    # Wait for rate limit period
    await asyncio.sleep(0.15)

    # Should be allowed again
    can_proceed = await rate_limiter.check_rate_limit(user_id)
    assert can_proceed is True


@pytest.mark.asyncio
async def test_different_users_have_separate_limits(rate_limiter):
    """Test that different users have separate rate limits."""
    user1_id = 12345
    user2_id = 67890

    # User 1 makes a request
    can_proceed = await rate_limiter.check_rate_limit(user1_id)
    assert can_proceed is True
    await rate_limiter.acquire(user1_id)

    # User 1 should be blocked
    can_proceed = await rate_limiter.check_rate_limit(user1_id)
    assert can_proceed is False

    # User 2 should still be allowed
    can_proceed = await rate_limiter.check_rate_limit(user2_id)
    assert can_proceed is True


def test_cleanup_old_limiters(rate_limiter):
    """Test cleanup of inactive user limiters."""
    # Create limiters for multiple users
    for user_id in [1, 2, 3, 4, 5]:
        rate_limiter.get_limiter(user_id)

    assert len(rate_limiter.limiters) == 5

    # Clean up, keeping only users 2 and 4
    active_users = {2, 4}
    rate_limiter.cleanup_old_limiters(active_users)

    assert len(rate_limiter.limiters) == 2
    assert 2 in rate_limiter.limiters
    assert 4 in rate_limiter.limiters
    assert 1 not in rate_limiter.limiters
    assert 3 not in rate_limiter.limiters
    assert 5 not in rate_limiter.limiters
