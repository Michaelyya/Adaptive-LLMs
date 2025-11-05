import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from main import AdaptiveLearningBenchmark
import config
MODELS = [
    {"name": "meta-llama/Llama-3.2-11B-Vision-Instruct", "type": "llama"},
    {"name": "meta-llama/Llama-3.2-90B-Vision", "type": "llama"},
    {"name": "meta-llama/Llama-4-Scout-17B-16E-Instruct", "type": "llama"},
    {"name": "gpt-4o", "type": "openai"},
    {"name": "gpt-5", "type": "openai"},
    {"name": "o1", "type": "openai"},
]


def run_single_evaluation(model_name: str, learner_profile: str, question_id: str):
    model_config = next((m for m in MODELS if m["name"] == model_name), None)
    benchmark = AdaptiveLearningBenchmark(output_dir=config.OUTPUTS_DIR)
    
    result = benchmark.run_evaluation(
        model_name=model_name,
        model_type=model_config["type"],
        learner_profile=learner_profile,
        question_id=question_id,
        save_intermediate=True
    )
    return result



def run_grade_evaluation(grade: int):
    from prompts.user_prompts import LEARNER_PROFILE_CONFIGS
    from data.question_data import get_questions_by_grade
    
    # Filter profiles by grade
    learner_profiles = {
        k: v for k, v in LEARNER_PROFILE_CONFIGS.items()
        if v.get("grade") == grade
    }
    questions = get_questions_by_grade(grade)
    
    print(f"\n{'='*60}")
    print(f"Running Grade {grade} Evaluation")
    print(f"Models: {len(MODELS)}")
    print(f"Learner Profiles: {len(learner_profiles)}")
    print(f"Questions: {len(questions)}")
    print(f"Total Combinations: {len(MODELS) * len(learner_profiles) * len(questions)}")
    print(f"{'='*60}\n")
    
    benchmark = AdaptiveLearningBenchmark(output_dir=config.OUTPUTS_DIR)
    
    for model_config in MODELS:
        for profile_id in learner_profiles.keys():
            for question_id in questions.keys():
                result = benchmark.run_evaluation(
                    model_name=model_config["name"],
                    model_type=model_config["type"],
                    learner_profile=profile_id,
                    question_id=question_id,
                    save_intermediate=True
                )
                print(f"✓ {model_config['name']} - {profile_id} - {question_id}")

    
    benchmark.save_summary()


def run_full_evaluation():
    print(f"\n{'='*60}")
    print("Starting FULL EVALUATION")
    print(f"Models: {len(MODELS)}")
    print(f"{'='*60}\n")
    
    benchmark = AdaptiveLearningBenchmark(output_dir=config.OUTPUTS_DIR)
    benchmark.run_full_evaluation(MODELS, save_summary=True)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run adaptive learning benchmark")
    parser.add_argument(
        "--mode",
        choices=["single", "grade", "full"],
        default="single",
        help="Evaluation mode"
    )
    parser.add_argument("--model", type=str, help="Model name")
    parser.add_argument("--profile", type=str, help="Learner profile")
    parser.add_argument("--question", type=str, help="Question ID")
    parser.add_argument("--grade", type=int, choices=[4, 8], help="Grade level")
    
    args = parser.parse_args()
    
    if args.mode == "single":
        if not all([args.model, args.profile, args.question]):
            print("Error: --model, --profile, and --question required for single mode")
            sys.exit(1)
        run_single_evaluation(args.model, args.profile, args.question)
    
    elif args.mode == "grade":
        if not args.grade:
            print("Error: --grade required for grade mode")
            sys.exit(1)
        run_grade_evaluation(args.grade)
    
    elif args.mode == "full":
        run_full_evaluation()
    
    else:
        print("Error: Unknown mode")
        sys.exit(1)
