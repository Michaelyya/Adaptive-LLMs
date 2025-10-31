"""
User prompts templates for the adaptive learning benchmark.
"""

def create_user_prompt(
    question_number: str,
    question_text: str,
    additional_context: str = ""
) -> str:

    prompt = f"Please solve and explain question {question_number}.\n"
    
    if question_text:
        prompt += f"\nQuestion: {question_text}\n"
    
    if additional_context:
        prompt += f"\n{additional_context}\n"
    
    prompt += "\nExplain your solution step by step, and make sure your explanation is appropriate for my learning level."
    
    return prompt


def create_open_ended_user_prompt(
    question_number: str,
    learner_context: dict
) -> str:
    prompt = f"Help me understand and solve this mathematics problem.\n"
    
    if "grade" in learner_context:
        prompt += f"I am in Grade {learner_context['grade']}.\n"
    
    prompt += f"\nThe problem is: {question_number}\n"
    
    prompt += "\nPlease explain the problem and help me work through it step by step."
    
    return prompt
