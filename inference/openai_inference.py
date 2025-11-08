import os
import base64
from typing import Dict, List, Optional
from openai import OpenAI
from pathlib import Path
from .base_inference import BaseInference, load_image
import dotenv
dotenv.load_dotenv()
class OpenAInference(BaseInference):
    SUPPORTED_MODELS = [
        "gpt-4o",
        "gpt-5",
        "o1",
    ]
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        super().__init__(model_name)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        self.client = OpenAI(api_key=self.api_key)
    
    
    def load_model(self):
        pass
    
    def _encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    def _prepare_image_content(self, images: List[str]) -> List[Dict]:
        """Prepare image content for API."""
        image_content = []
        
        for img in images:
            img_path = load_image(img)
            
            if img_path.startswith('http'):
                # URL image
                image_content.append({
                    "type": "image_url",
                    "image_url": {"url": img_path}
                })
            else:
                # Local file, encode to base64
                encoded_image = self._encode_image(img_path)
                image_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                })
        
        return image_content
    
    def generate(
        self,
        messages: List[Dict],
        images: Optional[List[str]] = None,
        max_new_tokens: int = 512,
        temperature: float = 1,
        **kwargs
    ) -> Dict:
        formatted_messages = []
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if images and role == "user":
                content_list = [{"type": "text", "text": content}]
                content_list.extend(self._prepare_image_content(images))
                formatted_messages.append({
                    "role": role,
                    "content": content_list
                })
            else:
                formatted_messages.append({
                    "role": role,
                    "content": content
                })
            requires_max_completion_tokens = (
            self.model_name.startswith("gpt-5") or 
            self.model_name.startswith("o1") or
            "2025" in self.model_name  # Models with 2025 in name typically need max_completion_tokens
        )
        
        valid_params = {
            "temperature": temperature,
            "top_p": kwargs.get("top_p"),
            "frequency_penalty": kwargs.get("frequency_penalty"),
            "presence_penalty": kwargs.get("presence_penalty"),
            "stream": kwargs.get("stream"),
            "stop": kwargs.get("stop"),
        }
                
        valid_params = {k: v for k, v in valid_params.items() if v is not None}
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=formatted_messages,
            **valid_params
        )
        
        return {
            "response": response.choices[0].message.content,
            "model": self.model_name,
            "tokens_used": response.usage.total_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens
        }


def create_openai_inference(model_name: str, api_key: Optional[str] = None) -> OpenAInference:
    inference = OpenAInference(model_name, api_key)
    inference.load_model()
    return inference
