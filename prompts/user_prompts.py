# Learner profile configurations
LEARNER_PROFILE_CONFIGS = {
    "profile_1": {
        "grade": 4,
        "likes_math": True,
        "confidence_level": "very confident",
        "mastered_topics": "all mathematics topics in grade 4, including number, measurement and geometry, and data",
        "timss_score": 615
    },
    "profile_2": {
        "grade": 4,
        "likes_math": False,
        "confidence_level": "not confident",
        "mastered_topics": "mathematics topics such as number and data in grade 4",
        "timss_score": 390
    },
    "profile_3": {
        "grade": 4,
        "likes_math": True,
        "confidence_level": "confident",
        "mastered_topics": "all mathematics topics in grade 4, including number, measurement and geometry, and data",
        "timss_score": 550
    },
    "profile_4": {
        "grade": 8,
        "likes_math": True,
        "confidence_level": "very confident",
        "mastered_topics": "all mathematics topics in grade 8, including number, algebra, geometry and measurement, and data and probability",
        "timss_score": 625
    },
    "profile_5": {
        "grade": 8,
        "likes_math": False,
        "confidence_level": "not confident",
        "mastered_topics": "mathematics topics such as number and geometry in grade 4",
        "timss_score": 390
    },
    "profile_6": {
        "grade": 8,
        "likes_math": True,
        "confidence_level": "very confident",
        "mastered_topics": "all mathematics topics in grade 8, including number, algebra, geometry and measurement, and data and probability",
        "timss_score": 550
    }
}


def get_user_prompt(profile_id: str) -> str:
    if profile_id not in LEARNER_PROFILE_CONFIGS:
        raise ValueError(f"Unknown profile_id: {profile_id}. Must be one of {list(LEARNER_PROFILE_CONFIGS.keys())}")
    
    config = LEARNER_PROFILE_CONFIGS[profile_id]
    
    # Build the introduction
    introduction = f"I am a student from Grade {config['grade']}, "
    
    # Add math attitude
    if config['likes_math']:
        introduction += "I like learning mathematics very much and "
    else:
        introduction += "I don't like learning mathematics and "
    
    # Add confidence level
    if config['confidence_level'] == "very confident":
        introduction += "I am very confident in mathematics. "
    elif config['confidence_level'] == "confident":
        introduction += "I am confident in mathematics. "
    else:  # not confident
        introduction += "I am not confident in mathematics. "
    
    # Add mastered topics
    introduction += f"Now I have mastered {config['mastered_topics']}. "
    
    # Add TIMSS score
    introduction += f"I got {config['timss_score']} in the TIMSS 2019 Math Test. "
    
    # Complete prompt
    return f"{introduction}Can you teach me this math question?"
