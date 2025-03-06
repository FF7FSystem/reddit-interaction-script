import asyncio
from typing import List

import asyncpraw
import asyncprawcore

from utils import custom_logger
from utils.models import IncomingArgs, Settings


class AsyncRedditInteraction:
    """Class to interact with Reddit API and fetch posts from a subreddit asynchronously."""

    def __init__(self) -> None:
        self.reddit = asyncpraw.Reddit(**Settings().model_dump())
        self.args = IncomingArgs()
        self.logger = custom_logger.setup_logger(self.__class__.__name__)

    async def __aenter__(self) -> 'AsyncRedditInteraction':
        """Establishes Reddit connection upon entering the context asynchronously."""
        try:
            await self.reddit.user.me()
            self.logger.info("Successfully connected to Reddit.")
            return self
        except asyncprawcore.exceptions.AsyncPrawcoreException as e:
            self.logger.error(f"Error during Reddit connection: {e}")
            raise

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        """Handles exceptions upon exiting the context asynchronously."""
        await self.reddit.close()
        if exc_type:
            self.logger.error(f"An error occurred: {exc_value}")

    def print_posts(self, posts: List) -> None:
        """Prints the fetched posts."""
        if posts:
            for post in posts:
                self.logger.info(f"Title: {post['title']} | Author: {post['author']} | Upvotes: {post['upvotes']}")
        else:
            self.logger.warning("No posts found or an error occurred.")

    async def fetch_posts(self, topic: str, limit: int = 5) -> List:
        """Fetches the latest posts from a subreddit asynchronously."""
        posts = []
        try:
            subreddit = await self.reddit.subreddit(topic, fetch=True)
            async for submission in subreddit.new(limit=limit):
                posts.append({
                    'title': submission.title,
                    'author': submission.author.name if submission.author else "Unknown",
                    'upvotes': submission.ups
                })
        except asyncprawcore.exceptions.TooManyRequests as e:
            self.logger.warning(f"Rate limit exceeded. Sleeping for {e.retry_after} seconds...")
            await asyncio.sleep(e.retry_after)
            posts = await self.fetch_posts(topic=topic, limit=limit)  # Retry fetching posts after sleeping
        except Exception as e:
            self.logger.error(f"An error occurred while fetching posts: {e}")
        return posts

    async def run(self) -> None:
        """Main method to run the Reddit interaction asynchronously."""
        posts = await self.fetch_posts(topic=self.args.topic, limit=self.args.limit)
        self.print_posts(posts)


if __name__ == "__main__":
    async def main():
        async with AsyncRedditInteraction() as reddit:
            await reddit.run()

    asyncio.run(main())

#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(AsyncRedditInteraction().main())

