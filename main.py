import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

from inference.llama_inference import create_llama_inference
from inference.openai_inference import create_openai_inference

from prompts.prompts import get_prompts_by_group, LEARNER_PROFILE_CONFIGS
from data.question_data import get_question, get_questions_by_grade


class AdaptiveLearningBenchmark:
    
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = []
    
    def create_messages(self, system_prompt: str, user_prompt: str, image_paths: List[str], group: int = 4) -> List[Dict]:
        # Create messages based on group configuration
        # Group 1: No prompts, only image
        # Group 2: Only user prompt
        # Group 3: System prompt (without TIMSS) + User prompt
        # Group 4: Full system prompt (with TIMSS) + User prompt
        
        messages = []
        
        if group == 1:
            # Group 1: Only image, no text prompts
            messages.append({"role": "user", "content": ""})
        elif group == 2:
            # Group 2: Only user prompt, no system prompt
            messages.append({"role": "user", "content": user_prompt or ""})
        else:
            # Groups 3 and 4: Both system and user prompts
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_prompt or ""})
        
        return messages
    
    def run_evaluation(self, model_name: str, model_type: str, learner_profile: str, question_id: str, 
                      group: int = 4, save_intermediate: bool = True) -> Dict:
        print(f"\n{'='*60}")
        print(f"Evaluating: {model_name}")
        print(f"Learner: {learner_profile}")
        print(f"Question: {question_id}")
        print(f"Group: {group}")
        print(f"{'='*60}\n")
        
        learner_data = LEARNER_PROFILE_CONFIGS.get(learner_profile, {})
        if not learner_data:
            raise ValueError(f"Unknown learner profile: {learner_profile}")
        
        question_data = get_question(question_id)
        system_prompt, user_prompt = get_prompts_by_group(group, learner_profile)
        
        # Prepare messages with image
        image_paths = [question_data["image_path"]]
        messages = self.create_messages(system_prompt, user_prompt, image_paths, group=group)
        
        # Load and run model
        if model_type == "llama":
            inference = create_llama_inference(model_name)
            result = inference.generate(messages=messages, images=image_paths)
        elif model_type == "openai":
            inference = create_openai_inference(model_name)
            result = inference.generate(messages=messages, images=image_paths)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Prepare result - Group 1 doesn't include prompts in output
        evaluation_result = {
            "timestamp": datetime.now().isoformat(),
            "model": model_name,
            "model_type": model_type,
            "learner_profile": learner_profile,
            "learner_data": learner_data,
            "question_id": question_id,
            "question_data": question_data,
            "group": group,
            "response": result["response"],
            "metadata": {k: v for k, v in result.items() if k != "response"}
        }
        
        # Only include prompts for groups 2, 3, 4 (not group 1)
        if group != 1:
            evaluation_result["system_prompt"] = system_prompt
            evaluation_result["user_prompt"] = user_prompt
        
        if save_intermediate:
            self.save_result(evaluation_result)
        
        self.results.append(evaluation_result)
        return evaluation_result
    
    def run_evaluation_with_inference(self, inference, model_name: str, model_type: str, 
                                     learner_profile: str, question_id: str, group: int = 4, 
                                     save_intermediate: bool = True) -> Dict:
        # Same as run_evaluation but uses pre-loaded inference instance for memory efficiency
        print(f"\n{'='*60}")
        print(f"Evaluating: {model_name}")
        print(f"Learner: {learner_profile}")
        print(f"Question: {question_id}")
        print(f"Group: {group}")
        print(f"{'='*60}\n")
        
        learner_data = LEARNER_PROFILE_CONFIGS.get(learner_profile, {})
        if not learner_data:
            raise ValueError(f"Unknown learner profile: {learner_profile}")
        
        question_data = get_question(question_id)
        system_prompt, user_prompt = get_prompts_by_group(group, learner_profile)
        
        image_paths = [question_data["image_path"]]
        messages = self.create_messages(system_prompt, user_prompt, image_paths, group=group)
        
        # Use pre-loaded inference instance
        result = inference.generate(messages=messages, images=image_paths)
        
        # Prepare result - Group 1 doesn't include prompts in output
        evaluation_result = {
            "timestamp": datetime.now().isoformat(),
            "model": model_name,
            "model_type": model_type,
            "learner_profile": learner_profile,
            "learner_data": learner_data,
            "question_id": question_id,
            "question_data": question_data,
            "group": group,
            "response": result["response"],
            "metadata": {k: v for k, v in result.items() if k != "response"}
        }
        
        # Only include prompts for groups 2, 3, 4 (not group 1)
        if group != 1:
            evaluation_result["system_prompt"] = system_prompt
            evaluation_result["user_prompt"] = user_prompt
        
        if save_intermediate:
            self.save_result(evaluation_result)
        
        self.results.append(evaluation_result)
        return evaluation_result
    
    def save_result(self, result: Dict):
        # Save single evaluation result to JSON file
        # Format: {group}_{model_name}_{profile}_{question}.json
        model_name = result['model'].replace('/', '_')
        filename = f"{result['group']}_{model_name}_{result['learner_profile']}_{result['question_id']}.json"
        
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Saved result to: {output_path}")
    
    def run_full_evaluation(self, models: List[Dict], save_summary: bool = True):
        # Run evaluation across all models, profiles, and questions
        print(f"\n{'='*60}")
        print("STARTING FULL EVALUATION")
        print(f"{'='*60}\n")
        
        learner_profiles = list(LEARNER_PROFILE_CONFIGS.keys())
        
        for model_config in models:
            model_name = model_config["name"]
            model_type = model_config["type"]
            
            for profile in learner_profiles:
                learner_data = LEARNER_PROFILE_CONFIGS.get(profile, {})
                if not learner_data:
                    continue
                
                grade = learner_data["grade"]
                questions = get_questions_by_grade(grade)
                
                for question_id, question_data in questions.items():
                    result = self.run_evaluation(
                        model_name=model_name,
                        model_type=model_type,
                        learner_profile=profile,
                        question_id=question_id
                    )
                    print(f"✓ Completed: {model_name} - {profile} - {question_id}")
        
        if save_summary:
            self.save_summary()
        
        print(f"\n{'='*60}")
        print("EVALUATION COMPLETE")
        print(f"Total results: {len(self.results)}")
        print(f"{'='*60}\n")
    
    def save_summary(self):
        # Save summary of all evaluations
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
    parser = argparse.ArgumentParser(description="Run adaptive learning LLM benchmark")
    parser.add_argument("--model", type=str, help="Specific model to evaluate (optional)")
    parser.add_argument("--profile", type=str, nargs='+', 
                       help="Specific learner profile(s) to evaluate (can specify multiple, space-separated or comma-separated)")
    parser.add_argument("--question", type=str, nargs='+', 
                       help="Specific question(s) to evaluate (can specify multiple, space-separated or comma-separated)")
    parser.add_argument("--output", type=str, default="outputs", help="Output directory")
    parser.add_argument("--full", action="store_true", help="Run full evaluation across all combinations")
    parser.add_argument("--group", type=str, nargs='+', default=["4"],
                       help="Prompt group(s) to evaluate (can specify multiple, space-separated or comma-separated: 1,2,3,4)")
    
    args = parser.parse_args()
    
    # Available models
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
        benchmark.run_full_evaluation(models)
    else:
        if args.model and args.profile and args.question:
            model_config = next((m for m in models if m["name"] == args.model), None)
            if not model_config:
                print(f"Error: Unknown model: {args.model}")
                return
            
            # Parse profiles: handle both space-separated and comma-separated
            profiles = []
            for p in args.profile:
                if ',' in p:
                    profiles.extend([p.strip() for p in p.split(',') if p.strip()])
                else:
                    profiles.append(p.strip())
            
            # Parse questions: handle both space-separated and comma-separated
            questions = []
            for q in args.question:
                if ',' in q:
                    questions.extend([q.strip() for q in q.split(',') if q.strip()])
                else:
                    questions.append(q.strip())
            
            # Parse groups: handle both space-separated and comma-separated
            groups = []
            for g in args.group:
                if ',' in g:
                    groups.extend([int(g.strip()) for g in g.split(',') if g.strip()])
                else:
                    groups.append(int(g.strip()))
            
            # Validate groups
            for g in groups:
                if g not in [1, 2, 3, 4]:
                    print(f"Error: Invalid group {g}. Must be 1, 2, 3, or 4.")
                    return
            
            # Load model once and reuse for all evaluations to save memory
            inference = None
            if model_config["type"] == "llama":
                inference = create_llama_inference(args.model)
            elif model_config["type"] == "openai":
                inference = create_openai_inference(args.model)
            
            # Run evaluation for each combination: profile -> question -> group
            total = len(profiles) * len(questions) * len(groups)
            current = 0
            print(f"\nRunning {total} evaluations: {len(profiles)} profiles × {len(questions)} questions × {len(groups)} groups\n")
            
            for profile in profiles:
                for question_id in questions:
                    for group in groups:
                        current += 1
                        result = benchmark.run_evaluation_with_inference(
                            inference=inference,
                            model_name=args.model,
                            model_type=model_config["type"],
                            learner_profile=profile,
                            question_id=question_id,
                            group=group
                        )
                        print(f"✓ [{current}/{total}] Completed: {args.model} - {profile} - {question_id} - Group {group}\n")
            
            # Clean up model after all evaluations
            if inference and hasattr(inference, 'cleanup'):
                inference.cleanup()
        else:
            print("Specify --model, --profile, and --question, or use --full for full evaluation")


if __name__ == "__main__":
    main()
