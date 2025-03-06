# Reddit Interaction Scripts

## Scripts
- `main.py` - in synchronous mode.
- `async_main.py`  - in asynchronous mode.

This script interacts with the Reddit API to fetch and display the latest posts from a specified subreddit. It utilizes the `praw\asyncpraw` library for API interactions and incorporates logging for better traceability. The script also includes basic handling of Reddit's rate limiting by implementing a simple retry mechanism.

## Prerequisites

Before running the script, ensure you have the following:

1. **Python 3.12**: The script has been tested with Python 3.12. Ensure you have this version installed.

2. **Required Python Libraries**:  
   These dependencies are listed in the `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Reddit API Credentials**: Obtain your Reddit API credentials by registering an application on [Reddit's developer portal](https://www.reddit.com/prefs/apps). You'll need the following:

   - `APP_NAME`: Name of your Reddit application
   - `APP_ID`: Client ID of your Reddit application
   - `APP_SECRET`: Client Secret of your Reddit application  
  

4. **`.env` File**: Create a `.env` file in the same directory as the script with the following content:

   ```env
   APP_NAME=your_app_name
   APP_ID=your_app_id
   APP_SECRET=your_app_secret
   ```

   Replace `your_app_name`, `your_app_id`, and `your_app_secret` with your actual Reddit API credentials.

## Usage

1. **Clone the Repository**: If you haven't already, clone the repository containing this script:

   ```bash
   git https://github.com/FF7FSystem/reddit-interaction-script
   cd reddit-interaction-script
   ```

2. **Set Up Virtual Environment (Optional but Recommended)**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use 'env\Scripts\activate'
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Script**:
   
   - `--topic`: Specifies the subreddit from which to fetch posts. This parameter is required.
   - `--limit`: Specifies the number of posts to fetch. This parameter is optional; if not provided, the script defaults to fetching 5 posts.  

   For example, to fetch the latest 5 posts from the "python" subreddit:

   ### In synchronous mode.  
   ```bash
   python main.py --topic "python" --limit 5
   ```
   #### In asynchronous mode.
   ```bash
   python async_main.py --topic "python" --limit 5
   ```   

   Or, to fetch the latest posts from the "learnpython" subreddit without specifying a limit (defaults to 5):

   ```bash
   python main.py --topic "learnpython"
   ```

## Rate Limit Handling

Reddit imposes rate limits on API requests to prevent abuse and ensure fair usage. In this script, a simple retry mechanism is implemented: if a rate limit is encountered, the script waits for 5 seconds before retrying the request. This basic approach is intended for simplicity and may not handle all rate limit scenarios gracefully.

For more robust rate limit handling, consider implementing a queue system using tools like Redis to manage and schedule API requests more effectively. However, this would introduce additional complexity and dependencies, which might not be necessary for simple interactions or testing purposes.

## Logging

The script uses Python's built-in `logging` module to provide informative messages about its operation. Logs include details about successful connections, fetched posts, and any errors encountered during execution. By default, logs are output to the console. You can configure the logging settings in the `setup_logger` method of the `RedditInteraction` class to direct logs to a file or adjust the log level.

## Notes

- **Error Handling**: The script includes basic error handling to catch and log exceptions that may occur during execution. However, it may not cover all edge cases. Enhance the error handling as needed based on your use case.

- **Customization**: Feel free to modify the script to suit your requirements, such as changing the logging configuration, adjusting the rate limit handling strategy, or extending functionality to interact with other Reddit API endpoints.

- **Reddit API Terms**: Ensure that your use of the Reddit API complies with [Reddit's API Terms of Use](https://www.redditinc.com/policies/data-api-terms). Be mindful of rate limits and usage policies to avoid potential issues.

By following these steps and considerations, you should be able to set up and run the Reddit Interaction script successfully. 