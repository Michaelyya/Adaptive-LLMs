"""
Base inference interface for all models.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional


class BaseInference(ABC):
    """Base class for all model inference implementations."""
    
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
        """
        Generate response from the model.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            images: List of image paths or URLs
            max_new_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional model-specific parameters
            
        Returns:
            Dictionary containing 'response', 'tokens_used', etc.
        """
        pass
    
    @abstractmethod
    def load_model(self):
        """Load the model into memory."""
        pass


def load_image(image_path: str) -> str:
    """Load image and return path or URL."""
    if image_path.startswith('http'):
        return image_path
    return str(Path(image_path).absolute())
