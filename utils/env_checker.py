import os

def check_env_file_exists(env_file_path: str = ".env"):
    """
    Check if the .env file exists in the specified path.
    Raise a RuntimeError if the file is missing.
    """
    if not os.path.isfile(env_file_path):
        raise RuntimeError(f"Environment file '{env_file_path}' is missing. Please create it and add the required environment variables.")
