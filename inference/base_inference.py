from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional


class BaseInference(ABC):
    
    def __init__(self, model_name: str):
        self.model_name = model_name
    
    @abstractmethod
    def generate(
        self,
        messages: List[Dict],
        images: Optional[List[str]] = None,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict:
        pass
    
    @abstractmethod
    def load_model(self):
        pass


def load_image(image_path: str) -> str:
    if image_path.startswith('http'):
        return image_path
    return str(Path(image_path).absolute())
