import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

from inference.llama_inference import create_llama_inference
from inference.openai_inference import create_openai_inference

from prompts.system_prompts import get_system_prompt_by_grade
from prompts.user_prompts import LEARNER_PROFILE_CONFIGS, get_user_prompt
# from prompts.parameters import get_generation_params

from data.question_data import get_question, get_questions_by_grade


class AdaptiveLearningBenchmark:
    
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = []
    
    def create_messages(
        self,
        system_prompt: str,
        user_prompt: str,
        image_paths: List[str]
    ) -> List[Dict]:
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        
        return messages
    
    def run_evaluation(
        self,
        model_name: str,
        model_type: str,
        learner_profile: str,
        question_id: str,
        save_intermediate: bool = True
    ) -> Dict:
        print(f"\n{'='*60}")
        print(f"Evaluating: {model_name}")
        print(f"Learner: {learner_profile}")
        print(f"Question: {question_id}")
        print(f"{'='*60}\n")
        
        learner_data = LEARNER_PROFILE_CONFIGS.get(learner_profile, {})
        if not learner_data:
            raise ValueError(f"Unknown learner profile: {learner_profile}")
        
        question_data = get_question(question_id)
        
        # Use grade-specific system prompt for concise, targeted guidance
        system_prompt = get_system_prompt_by_grade(learner_data.get("grade"))
        user_prompt = get_user_prompt(learner_profile)
        
        # generation_params = get_generation_params(learner_profile)
        
        # Prepare messages
        image_paths = [question_data["image_path"]]
        messages = self.create_messages(system_prompt, user_prompt, image_paths)
        
        # Load and run model
        if model_type == "llama":
            inference = create_llama_inference(model_name)
            result = inference.generate(
                messages=messages,
                images=image_paths,
                # **generation_params
            )
        elif model_type == "openai":
            inference = create_openai_inference(model_name)
            result = inference.generate(
                messages=messages,
                images=image_paths,
                # **generation_params
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Prepare result
        evaluation_result = {
            "timestamp": datetime.now().isoformat(),
            "model": model_name,
            "model_type": model_type,
            "learner_profile": learner_profile,
            "learner_data": learner_data,
            "question_id": question_id,
            "question_data": question_data,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            # "generation_params": generation_params,
            "response": result["response"],
            "metadata": {
                k: v for k, v in result.items() if k != "response"
            }
        }
        
        # Save intermediate result if requested
        if save_intermediate:
            self.save_result(evaluation_result)
        
        self.results.append(evaluation_result)
        return evaluation_result
    
    def run_evaluation_with_inference(
        self,
        inference,
        model_name: str,
        model_type: str,
        learner_profile: str,
        question_id: str,
        save_intermediate: bool = True
    ) -> Dict:
        """Run evaluation using a pre-loaded inference instance (for memory efficiency)."""
        print(f"\n{'='*60}")
        print(f"Evaluating: {model_name}")
        print(f"Learner: {learner_profile}")
        print(f"Question: {question_id}")
        print(f"{'='*60}\n")
        
        learner_data = LEARNER_PROFILE_CONFIGS.get(learner_profile, {})
        if not learner_data:
            raise ValueError(f"Unknown learner profile: {learner_profile}")
        
        question_data = get_question(question_id)
        
        # Use grade-specific system prompt for concise, targeted guidance
        system_prompt = get_system_prompt_by_grade(learner_data.get("grade"))
        user_prompt = get_user_prompt(learner_profile)
        
        # Prepare messages
        image_paths = [question_data["image_path"]]
        messages = self.create_messages(system_prompt, user_prompt, image_paths)
        
        # Use pre-loaded inference instance
        result = inference.generate(
            messages=messages,
            images=image_paths,
        )
        
        # Prepare result
        evaluation_result = {
            "timestamp": datetime.now().isoformat(),
            "model": model_name,
            "model_type": model_type,
            "learner_profile": learner_profile,
            "learner_data": learner_data,
            "question_id": question_id,
            "question_data": question_data,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "response": result["response"],
            "metadata": {
                k: v for k, v in result.items() if k != "response"
            }
        }
        
        # Save intermediate result if requested
        if save_intermediate:
            self.save_result(evaluation_result)
        
        self.results.append(evaluation_result)
        return evaluation_result
    
    def save_result(self, result: Dict):
        """Save a single result to a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = (
            f"{result['model'].replace('/', '_')}_"
            f"{result['learner_profile']}_"
            f"{result['question_id']}_"
            f"{timestamp}.json"
        )
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Saved result to: {output_path}")
    
    def run_full_evaluation(
        self,
        models: List[Dict],
        save_summary: bool = True
    ):
        """
        Run full evaluation across all models, learners, and questions.
        
        Args:
            models: List of model configurations
            save_summary: Whether to save a summary of all results
        """
        print(f"\n{'='*60}")
        print("STARTING FULL EVALUATION")
        print(f"{'='*60}\n")
        
        # Get all learner profiles (using the 6 profiles from user_prompts)
        learner_profiles = list(LEARNER_PROFILE_CONFIGS.keys())
        
        # Run evaluation for each combination
        for model_config in models:
            model_name = model_config["name"]
            model_type = model_config["type"]
            
            for profile in learner_profiles:
                learner_data = LEARNER_PROFILE_CONFIGS.get(profile, {})
                if not learner_data:
                    continue
                grade = learner_data["grade"]
                
                # Get questions for this grade
                questions = get_questions_by_grade(grade)
                
                for question_id, question_data in questions.items():
                    try:
                        result = self.run_evaluation(
                            model_name=model_name,
                            model_type=model_type,
                            learner_profile=profile,
                            question_id=question_id
                        )
                        
                        print(f"✓ Completed: {model_name} - {profile} - {question_id}")
                        
                    except Exception as e:
                        print(f"✗ Failed: {model_name} - {profile} - {question_id}")
                        print(f"  Error: {str(e)}\n")
        
        if save_summary:
            self.save_summary()
        
        print(f"\n{'='*60}")
        print("EVALUATION COMPLETE")
        print(f"Total results: {len(self.results)}")
        print(f"{'='*60}\n")
    
    def save_summary(self):
        summary = {
            "total_evaluations": len(self.results),
            "timestamp": datetime.now().isoformat(),
            "results": [
                {
                    "model": r["model"],
                    "learner": r["learner_profile"],
                    "question": r["question_id"],
                    "timestamp": r["timestamp"]
                }
                for r in self.results
            ]
        }
        
        summary_path = self.output_dir / "summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Saved summary to: {summary_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Run adaptive learning LLM benchmark"
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Specific model to evaluate (optional)"
    )
    parser.add_argument(
        "--profile",
        type=str,
        nargs='+',
        help="Specific learner profile(s) to evaluate (can specify multiple, space-separated or comma-separated)"
    )
    parser.add_argument(
        "--question",
        type=str,
        nargs='+',
        help="Specific question(s) to evaluate (can specify multiple, space-separated or comma-separated)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="outputs",
        help="Output directory"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Run full evaluation across all combinations"
    )
    
    args = parser.parse_args()
    
    # Define models to evaluate
    models = [
        {"name": "meta-llama/Llama-3.2-11B-Vision-Instruct", "type": "llama"},
        {"name": "meta-llama/Llama-3.2-90B-Vision-Instruct", "type": "llama"},
        {"name": "meta-llama/Llama-4-Scout-17B-16E-Instruct", "type": "llama"},
        {"name": "gpt-4o", "type": "openai"},
        {"name": "gpt-5", "type": "openai"},
        {"name": "o1", "type": "openai"},
    ]
    
    benchmark = AdaptiveLearningBenchmark(output_dir=args.output)
    
    if args.full:
        # Run full evaluation
        benchmark.run_full_evaluation(models)
    else:
        # Run specific evaluation
        if args.model and args.profile and args.question:
            model_config = next((m for m in models if m["name"] == args.model), None)
            if not model_config:
                print(f"Error: Unknown model: {args.model}")
                return
            
            # Parse profiles: handle both space-separated and comma-separated
            profiles = []
            for p in args.profile:
                # Split by comma if comma-separated
                if ',' in p:
                    profiles.extend([p.strip() for p in p.split(',') if p.strip()])
                else:
                    profiles.append(p.strip())
            
            # Parse questions: handle both space-separated and comma-separated
            questions = []
            for q in args.question:
                # Split by comma if comma-separated
                if ',' in q:
                    questions.extend([q.strip() for q in q.split(',') if q.strip()])
                else:
                    questions.append(q.strip())
            
            # Reuse model instance for multiple evaluations to save memory
            inference = None
            try:
                # Load model once for all evaluations
                if model_config["type"] == "llama":
                    from inference.llama_inference import create_llama_inference
                    inference = create_llama_inference(args.model)
                elif model_config["type"] == "openai":
                    from inference.openai_inference import create_openai_inference
                    inference = create_openai_inference(args.model)
                
                # Run evaluation for each combination of profile and question
                for profile in profiles:
                    for question_id in questions:
                        try:
                            # Use the pre-loaded model instance
                            result = benchmark.run_evaluation_with_inference(
                                inference=inference,
                                model_name=args.model,
                                model_type=model_config["type"],
                                learner_profile=profile,
                                question_id=question_id
                            )
                            print(f"✓ Completed: {args.model} - {profile} - {question_id}\n")
                        except Exception as e:
                            print(f"✗ Failed: {args.model} - {profile} - {question_id}")
                            print(f"  Error: {str(e)}\n")
            finally:
                # Clean up model after all evaluations
                if inference and hasattr(inference, 'cleanup'):
                    inference.cleanup()
        else:
            print("Specify --model, --profile, and --question, or use --full for full evaluation")


if __name__ == "__main__":
    main()

