import os

# Instead of importing from a local config file, use environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Now you can use OPENAI_API_KEY in your code as usual
