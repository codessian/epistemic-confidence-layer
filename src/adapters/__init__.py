# Import all adapters to ensure they register themselves
from . import openai
from . import anthropic
from . import google
from . import openrouter
from . import ollama
from . import hf
from . import gemini
from . import vertex