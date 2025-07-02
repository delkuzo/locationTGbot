"""Rate limiting service for the bot."""

import logging

from aiolimiter import AsyncLimiter

from config.settings import settings

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter for user requests."""

    def __init__(self):
        """Initialize rate limiter."""
        self.limiters: dict[int, AsyncLimiter] = {}
        self.max_rate = settings.rate_limit_requests
        self.time_period = settings.rate_limit_period

    def get_limiter(self, user_id: int) -> AsyncLimiter:
        """
        Get or create limiter for a specific user.

        Args:
            user_id: Telegram user ID

        Returns:
            AsyncLimiter instance for the user
        """
        if user_id not in self.limiters:
            self.limiters[user_id] = AsyncLimiter(
                max_rate=self.max_rate, time_period=self.time_period
            )
        return self.limiters[user_id]

    async def check_rate_limit(self, user_id: int) -> bool:
        """
        Check if user can make a request.

        Args:
            user_id: Telegram user ID

        Returns:
            True if request is allowed, False otherwise
        """
        limiter = self.get_limiter(user_id)
        return limiter.has_capacity()

    async def acquire(self, user_id: int) -> None:
        """
        Acquire a slot for the user request.

        Args:
            user_id: Telegram user ID
        """
        limiter = self.get_limiter(user_id)
        await limiter.acquire()

    def cleanup_old_limiters(self, active_users: set) -> None:
        """
        Remove limiters for inactive users to free memory.

        Args:
            active_users: Set of currently active user IDs
        """
        inactive_users = set(self.limiters.keys()) - active_users
        for user_id in inactive_users:
            del self.limiters[user_id]

        if inactive_users:
            logger.info(f"Cleaned up {len(inactive_users)} inactive user limiters")


# Create singleton instance
rate_limiter = RateLimiter()
