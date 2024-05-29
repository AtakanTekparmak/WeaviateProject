import tomllib

# Declare constants
CONFIG_PATH = "config.toml"

def load_toml_file(path: str) -> dict:
    """
    Load a TOML file and return it as a dictionary.
    """
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    
def load_config() -> dict:
    """
    Load the configuration file and return it as a dictionary.
    """
    return load_toml_file(CONFIG_PATH)

if __name__ == "__main__":
    config = load_config()
    print(config)