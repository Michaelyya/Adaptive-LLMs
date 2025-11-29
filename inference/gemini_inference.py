import os
import base64
from typing import Dict, List, Optional
from pathlib import Path
from .base_inference import BaseInference, load_image
import dotenv
dotenv.load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class GeminiInference(BaseInference):
    SUPPORTED_MODELS = [
        "gemini-2.5-pro",
    ]
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        super().__init__(model_name)
        if genai is None:
            raise ImportError("google-generativeai package is required. Install with: pip install google-generativeai")
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def load_model(self):
        pass
    
    def _load_image_for_gemini(self, image_path: str):
        """Load image for Gemini API."""
        img_path = load_image(image_path)
        
        if img_path.startswith('http'):
            # For URL images, download first or use PIL
            import urllib.request
            from PIL import Image
            import io
            with urllib.request.urlopen(img_path) as response:
                image_data = response.read()
            return Image.open(io.BytesIO(image_data))
        else:
            # Local file
            from PIL import Image
            return Image.open(img_path)
    
    def generate(self, messages: List[Dict], images: Optional[List[str]] = None,
                 max_new_tokens: int = 512, temperature: float = 0.7, **kwargs) -> Dict:
        # Build content for Gemini
        content_parts = []
        
        # Extract system and user messages
        system_text = ""
        user_text = ""
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                system_text = content
            elif role == "user":
                user_text = content
        
        # Combine system and user text
        full_prompt = ""
        if system_text:
            full_prompt = f"{system_text}\n\n{user_text}"
        else:
            full_prompt = user_text
        
        content_parts.append(full_prompt)
        
        # Add images
        if images:
            for img in images:
                pil_image = self._load_image_for_gemini(img)
                content_parts.append(pil_image)
        
        # Configure generation
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=max(max_new_tokens, 2048),
            temperature=temperature,
        )
        
        if kwargs.get("top_p"):
            generation_config.top_p = kwargs.get("top_p")
        if kwargs.get("top_k"):
            generation_config.top_k = kwargs.get("top_k")
        
        # Call Gemini API
        response = self.model.generate_content(
            content_parts,
            generation_config=generation_config
        )
        
        # Debug logging to inspect raw response structure when Gemini returns no text
        print("\n[GEMINI DEBUG] Raw response:", response)
        candidates = getattr(response, "candidates", None) or []
        for idx, cand in enumerate(candidates):
            finish_reason = getattr(cand, "finish_reason", None)
            safety = getattr(cand, "safety_ratings", None)
            print(f"[GEMINI DEBUG] Candidate {idx} finish_reason: {finish_reason}")
            print(f"[GEMINI DEBUG] Candidate {idx} safety_ratings: {safety}")
        
        # Extract response text safely (Gemini may return no Parts when finish_reason != OK)
        response_text = ""
        try:
            if hasattr(response, "text") and response.text:
                response_text = response.text
        except Exception:
            # Fall back to empty string if quick accessor fails
            response_text = ""
        
        # Get token counts if available
        tokens_used = None
        prompt_tokens = None
        completion_tokens = None
        
        if hasattr(response, "usage_metadata"):
            prompt_tokens = getattr(response.usage_metadata, "prompt_token_count", None)
            completion_tokens = getattr(response.usage_metadata, "candidates_token_count", None)
            if prompt_tokens is not None and completion_tokens is not None:
                tokens_used = prompt_tokens + completion_tokens
        
        return {
            "response": response_text,
            "model": self.model_name,
            "tokens_used": tokens_used,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens
        }


def create_gemini_inference(model_name: str, api_key: Optional[str] = None) -> GeminiInference:
    inference = GeminiInference(model_name, api_key)
    inference.load_model()
    return inference

