import os
from dotenv import load_dotenv


def load_env(project_name='graphrag-contract-review', env_stage="dev"):
    home = os.path.expanduser("~")
    env_file = f"{env_stage}.env"
    env_path = os.path.join(home, ".env_configs", project_name, env_file)

    # Load shared env if needed
    shared_path = os.path.join(home, ".env_configs", "shared.env")
    if os.path.exists(shared_path):
        load_dotenv(dotenv_path=shared_path)

    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path, override=True)
    else:
        raise FileNotFoundError(f"{env_path} not found")


load_env("graphrag-contract-review", "dev")


def get_env_variable(key):
    return os.getenv(key)


if __name__ == '__main__':
    print(get_env_variable('OPENAI_API_KEY'))
