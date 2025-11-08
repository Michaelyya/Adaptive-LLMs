"""
Parameters and constants for the adaptive learning benchmark.
"""

# Generation parameters
GENERATION_PARAMS = {
    "max_new_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.95,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}

# # Per-learner-profile parameters
# LEARNER_PARAMS = {
#     "grade4_high": {
#         "max_new_tokens": 600,
#         "temperature": 0.8,
#         "encourage_deeper_explanation": True
#     },
#     "grade4_middle": {
#         "max_new_tokens": 512,
#         "temperature": 0.7,
#         "encourage_deeper_explanation": False
#     },
#     "grade4_low": {
#         "max_new_tokens": 400,
#         "temperature": 0.6,
#         "encourage_deeper_explanation": False
#     },
#     "grade8_high": {
#         "max_new_tokens": 700,
#         "temperature": 0.8,
#         "encourage_deeper_explanation": True
#     },
#     "grade8_middle": {
#         "max_new_tokens": 600,
#         "temperature": 0.7,
#         "encourage_deeper_explanation": False
#     },
#     "grade8_low": {
#         "max_new_tokens": 500,
#         "temperature": 0.6,
#         "encourage_deeper_explanation": False
#     },
# }


# def get_generation_params(learner_profile: str) -> dict:
#     """
#     Get generation parameters for a specific learner profile.
    
#     Args:
#         learner_profile: Learner profile identifier
        
#     Returns:
#         Dictionary of generation parameters
#     """
#     return LEARNER_PARAMS.get(
#         learner_profile,
#         GENERATION_PARAMS
#     ).copy()
