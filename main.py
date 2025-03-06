import time
from typing import List

import praw
import praw.exceptions as praw_exceptions

from utils import custom_logger
from utils.models import IncomingArgs, Settings


class RedditInteraction:
    """Class to interact with Reddit API and fetch posts from a subreddit."""

    def __init__(self) -> None:
        self.reddit = praw.Reddit(**Settings().model_dump())
        self.args = IncomingArgs()
        self.logger = custom_logger.setup_logger(self.__class__.__name__)

    def __enter__(self) -> 'RedditInteraction':
        """Establishes Reddit connection upon entering the context."""
        try:
            self.reddit.user.me()
            self.logger.info("Successfully connected to Reddit.")
            return self
        except praw_exceptions.PRAWException as e:
            self.logger.error(f"Error during Reddit connection: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        """Handles exceptions upon exiting the context."""
        if exc_type:
            self.logger.error(f"An error occurred: {exc_value}")
        return False  # Propagate the exception if any

    def print_posts(self, posts: List) -> None:
        """Prints the fetched posts."""
        if posts:
            for post in posts:
                self.logger.info(f"Title: {post['title']} | Author: {post['author']} | Upvotes: {post['upvotes']}")
        else:
            self.logger.warning("No posts found or an error occurred.")

    def fetch_posts(self, topic: str, limit: int = 5) -> List:
        """Fetches the latest posts from a subreddit."""
        posts = []
        try:
            for submission in self.reddit.subreddit(topic).new(limit=limit):
                posts.append({
                    'title': submission.title,
                    'author': submission.author.name if submission.author else "Unknown",
                    'upvotes': submission.ups
                })
        except praw_exceptions.RedditAPIException as e:
            if 'RATELIMIT' in str(e):
                self.logger.warning("Rate limit exceeded. Sleeping for 5 seconds...")
                time.sleep(5)
                posts = self.fetch_posts(topic=topic, limit=limit)  # Retry fetching posts after sleeping
            else:
                self.logger.error(f"Reddit API error: {e}")
        except Exception as e:
            self.logger.error(f"An error occurred while fetching posts: {e}")
        return posts

    def run(self) -> None:
        """Main method to run the Reddit interaction."""
        posts = self.fetch_posts(topic=self.args.topic, limit=self.args.limit)
        self.print_posts(posts)


if __name__ == "__main__":
    with RedditInteraction() as reddit:
        reddit.run()
