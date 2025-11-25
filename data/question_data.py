# Grade 4 Questions
GRADE4_QUESTIONS = {
    "G4Q1": {
        "question_number": "G4Q1",
        # "domain": "number",
        # "description": "Place value and number operations",
        "image_path": "pics/G4Q1.PNG"
    },
    "G4Q2": {
        "question_number": "G4Q2",
        # "domain": "measurement",
        # "description": "Measuring and comparing lengths",
        "image_path": "pics/G4Q2.PNG"
    },
    "G4Q3": {
        "question_number": "G4Q3",
        # "domain": "data",
        # "description": "Reading and interpreting data from graphs",
        "image_path": "pics/G4Q3.PNG"
    },
    "G4Q4": {
        "question_number": "G4Q4",
        # "domain": "data",
        # "description": "Data analysis",
        "image_path": "pics/G4Q4.PNG"
    },
    "G4Q5": {
        "question_number": "G4Q5",
        # "domain": "data",
        # "description": "Data analysis",
        "image_path": "pics/G4Q5.png"
    }
}

# Grade 8 Questions
GRADE8_QUESTIONS = {
    "G8Q1": {
        "question_number": "G8Q1",
        # "domain": "number",
        # "description": "Operations with rational numbers",
        "image_path": "pics/G8Q1.PNG"
    },
    "G8Q2": {
        "question_number": "G8Q2",
        # "domain": "algebra",
        # "description": "Linear equations and expressions",
        "image_path": "pics/G8Q2.PNG"
    },
    "G8Q3": {
        "question_number": "G8Q3",
        # "domain": "geometry_measurement",
        # "description": "Geometric properties and measurement",
        "image_path": "pics/G8Q3.PNG"
    },
    "G8Q4": {
        "question_number": "G8Q4",
        # "domain": "data_probability",
        # "description": "Data analysis and probability",
        "image_path": "pics/G8Q4.png"
    },
    "G8Q5": {
        "question_number": "G8Q5",
        # "domain": "data_probability",
        # "description": "Data analysis and probability",
        "image_path": "pics/G8Q5.png"
    }
}


def get_question(question_id: str) -> dict:
    all_questions = {**GRADE4_QUESTIONS, **GRADE8_QUESTIONS}
    return all_questions.get(question_id, {})


def get_questions_by_grade(grade: int) -> dict:
    if grade == 4:
        return GRADE4_QUESTIONS.copy()
    elif grade == 8:
        return GRADE8_QUESTIONS.copy()
    else:
        return {}


# def get_questions_by_domain(domain: str) -> dict:
#     """
#     Get all questions for a specific domain.
#     
#     Args:
#         domain: Mathematics domain
#         
#     Returns:
#         Dictionary of questions for the domain
#     """
#     all_questions = {**GRADE4_QUESTIONS, **GRADE8_QUESTIONS}
#     return {
#         k: v for k, v in all_questions.items()
#         if v.get("domain") == domain
#     }
