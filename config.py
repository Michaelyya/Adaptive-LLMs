import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
INFERENCE_DIR = PROJECT_ROOT / "inference"
PICS_DIR = PROJECT_ROOT / "pics"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Create directories if they don't exist
for directory in [DATA_DIR, PROMPTS_DIR, INFERENCE_DIR, PICS_DIR, OUTPUTS_DIR]:
    directory.mkdir(exist_ok=True)

# Model configurations
MODELS = {
    "llama": [
        {
            "name": "meta-llama/Llama-3.2-11B-Vision-Instruct",
            "type": "llama",
            "description": "Llama 3.2 11B Vision Instruct"
        },
        {
            "name": "Qwen/Qwen3-VL-30B-A3B-Instruct",
            "type": "llama",
            "description": "Qwen3 VL 30B A3B Instruct"
        }
    ],
    "openai": [
        {
            "name": "gpt-5",
            "type": "openai",
            "description": "GPT-5"
        },
        {
            "name": "o1",
            "type": "openai",
            "description": "O1"
        }
    ],
    "claude": [
        {
            "name": "claude-sonnet-4-20250514",
            "type": "claude",
            "description": "Claude Sonnet 4"
        }
    ]
}


# API Keys - loaded from .env file or environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
HUGGINGFACE_TOKEN = os.getenv("Huggingface_API_KEY", "") or os.getenv("HUGGINGFACE_TOKEN", "")

# Device configuration
DEVICE = "auto"  # or "cuda", "cpu", "mps"

# Default generation parameters
DEFAULT_MAX_TOKENS = 512
DEFAULT_TEMPERATURE = 0.7

# Output configuration
SAVE_INTERMEDIATE_RESULTS = True
RESULT_FILE_FORMAT = "json"
