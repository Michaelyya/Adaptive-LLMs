import torch
from transformers import AutoProcessor, AutoModelForVision2Seq
from pathlib import Path
from typing import Dict, List, Optional
from .base_inference import BaseInference, load_image
from config import HUGGINGFACE_TOKEN

class LlamaInference(BaseInference):   
    MODEL_CONFIGS = {
        "meta-llama/Llama-3.2-11B-Vision-Instruct": {
            "processor_class": "AutoProcessor",
            "model_class": "AutoModelForVision2Seq"
        },
        "meta-llama/Llama-3.2-90B-Vision": {
            "processor_class": "AutoProcessor",
            "model_class": "AutoModelForVision2Seq"
        },
        "meta-llama/Llama-4-Scout-17B-16E-Instruct": {
            "processor_class": "AutoProcessor",
            "model_class": "Llama4ForConditionalGeneration",
            "special_attn": "flex_attention"
        }
    }
    
    def __init__(self, model_name: str, device_map: str = "auto"):
        super().__init__(model_name)
        self.device_map = device_map
        self.model = None
        self.processor = None
        self._validate_model()
    
    def _validate_model(self):
        if self.model_name not in self.MODEL_CONFIGS:
            raise ValueError(f"Unsupported model: {self.model_name}")
    
    def load_model(self):
        config = self.MODEL_CONFIGS[self.model_name]
        
        token = HUGGINGFACE_TOKEN
        token_kwargs = {"token": token} if token else {}
        
        self.processor = AutoProcessor.from_pretrained(
            self.model_name,
            **token_kwargs
        )
        
        # Load model based on model_class
        if config["model_class"] == "AutoModelForVision2Seq":
            self.model = AutoModelForVision2Seq.from_pretrained(
                self.model_name,
                device_map=self.device_map,
                torch_dtype=torch.bfloat16,
                **token_kwargs
            )
        elif "Llama4ForConditionalGeneration" in config.get("model_class", ""):
            from transformers import Llama4ForConditionalGeneration
            kwargs = {
                "device_map": self.device_map,
                "torch_dtype": torch.bfloat16,
                **token_kwargs
            }
            if "special_attn" in config:
                kwargs["attn_implementation"] = config["special_attn"]
            
            self.model = Llama4ForConditionalGeneration.from_pretrained(
                self.model_name,
                **kwargs
            )
        else:
            raise ValueError(f"Unsupported model class: {config.get('model_class')}")
    
    def generate(
        self,
        messages: List[Dict],
        images: Optional[List[str]] = None,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict:

        if self.model is None or self.processor is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        processed_images = []
        if images:
            for img in images:
                processed_images.append(load_image(img))
        
        # Format messages for processing
        formatted_messages = self._format_messages(messages, processed_images)
        
        # Apply chat template
        inputs = self.processor.apply_chat_template(
            formatted_messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)
        
        # Filter valid generation parameters
        valid_params = {
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "top_p": kwargs.get("top_p"),
            "top_k": kwargs.get("top_k"),
            "do_sample": kwargs.get("do_sample", True if temperature > 0 else False),
            "repetition_penalty": kwargs.get("repetition_penalty"),
            "num_beams": kwargs.get("num_beams"),
        }
        generate_kwargs = {k: v for k, v in valid_params.items() if v is not None}
        
        outputs = self.model.generate(**inputs, **generate_kwargs)
        
        response = self.processor.batch_decode(
            outputs[:, inputs["input_ids"].shape[-1]:]
        )[0]
        
        return {
            "response": response,
            "model": self.model_name,
            "tokens_generated": len(outputs[0]) - inputs["input_ids"].shape[-1]
        }
    
    def _format_messages(self, messages: List[Dict], images: List[str]) -> List[Dict]:
        formatted = []
        
        for msg in messages:
            if isinstance(msg.get("content"), list):
                formatted.append(msg)
            else:
                formatted.append({
                    "role": msg.get("role", "user"),
                    "content": [
                        {"type": "text", "text": msg.get("content", "")}
                    ]
                })
        
        if images and formatted:
            last_msg = formatted[-1]
            if isinstance(last_msg.get("content"), list):
                for img in images:
                    last_msg["content"].insert(
                        -1,  # Before the last text element
                        {"type": "image", "url": img}
                    )
        
        return formatted


def create_llama_inference(model_name: str) -> LlamaInference:
    inference = LlamaInference(model_name)
    inference.load_model()
    return inference
