import os
import base64
from typing import Dict, List, Optional
from anthropic import Anthropic
from pathlib import Path
from .base_inference import BaseInference, load_image
import dotenv
dotenv.load_dotenv()

class ClaudeInference(BaseInference):
    SUPPORTED_MODELS = [
        "claude-sonnet-4-20250514",
    ]
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        super().__init__(model_name)
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)
    
    def load_model(self):
        pass
    
    def _encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    def _prepare_image_content(self, images: List[str]) -> List[Dict]:
        # Prepare image content for Claude API
        image_content = []
        
        for img in images:
            img_path = load_image(img)
            
            if img_path.startswith('http'):
                # URL image - Claude supports URLs
                image_content.append({
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": img_path
                    }
                })
            else:
                # Local file, encode to base64
                encoded_image = self._encode_image(img_path)
                # Determine media type from file extension
                media_type = "image/jpeg"
                if img_path.lower().endswith('.png'):
                    media_type = "image/png"
                elif img_path.lower().endswith('.gif'):
                    media_type = "image/gif"
                elif img_path.lower().endswith('.webp'):
                    media_type = "image/webp"
                
                image_content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": encoded_image
                    }
                })
        
        return image_content
    
    def generate(self, messages: List[Dict], images: Optional[List[str]] = None,
                 max_new_tokens: int = 512, temperature: float = 0.7, **kwargs) -> Dict:
        # Format messages for Claude API
        formatted_messages = []
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            # Claude uses "assistant" instead of "system"
            if role == "system":
                # Claude doesn't have system messages, so we prepend it to the first user message
                if not formatted_messages or formatted_messages[-1].get("role") != "user":
                    formatted_messages.append({"role": "user", "content": []})
                if isinstance(formatted_messages[-1]["content"], list):
                    formatted_messages[-1]["content"].insert(0, {"type": "text", "text": content})
                else:
                    formatted_messages[-1]["content"] = [{"type": "text", "text": content}]
            else:
                # User or assistant message
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
        
        # Prepare parameters
        valid_params = {
            "max_tokens": max_new_tokens,
            "temperature": temperature,
        }
        
        # Add optional parameters
        if kwargs.get("top_p"):
            valid_params["top_p"] = kwargs.get("top_p")
        if kwargs.get("top_k"):
            valid_params["top_k"] = kwargs.get("top_k")
        
        valid_params = {k: v for k, v in valid_params.items() if v is not None}
        
        # Call Claude API
        response = self.client.messages.create(
            model=self.model_name,
            messages=formatted_messages,
            **valid_params
        )
        
        # Extract response text
        response_text = ""
        if response.content:
            for content_block in response.content:
                if hasattr(content_block, 'text'):
                    response_text += content_block.text
        
        return {
            "response": response_text,
            "model": self.model_name,
            "tokens_used": response.usage.input_tokens + response.usage.output_tokens if hasattr(response, 'usage') else None,
            "prompt_tokens": response.usage.input_tokens if hasattr(response, 'usage') else None,
            "completion_tokens": response.usage.output_tokens if hasattr(response, 'usage') else None
        }


def create_claude_inference(model_name: str, api_key: Optional[str] = None) -> ClaudeInference:
    inference = ClaudeInference(model_name, api_key)
    inference.load_model()
    return inference

