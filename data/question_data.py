"""
Question data for TIMSS 2019 mathematics questions.

Note: Actual TIMSS question data should be added here based on TIMSS database.
"""

# Grade 4 Questions
# Domain: Number, Measurement, Data
GRADE4_QUESTIONS = {
    "G4Q1": {
        "question_number": "TIMSS-2019-4-M01",
        "domain": "number",
        "description": "Place value and number operations",
        "image_path": "pics/grade4_q1.png"
    },
    "G4Q2": {
        "question_number": "TIMSS-2019-4-M02",
        "domain": "measurement",
        "description": "Measuring and comparing lengths",
        "image_path": "pics/grade4_q2.png"
    },
    "G4Q3": {
        "question_number": "TIMSS-2019-4-M03",
        "domain": "data",
        "description": "Reading and interpreting data from graphs",
        "image_path": "pics/grade4_q3.png"
    }
}

# Grade 8 Questions
# Domain: Number, Algebra, Geometry and Measurement, Data and Probability
GRADE8_QUESTIONS = {
    "G8Q1": {
        "question_number": "TIMSS-2019-8-M01",
        "domain": "number",
        "description": "Operations with rational numbers",
        "image_path": "pics/grade8_q1.png"
    },
    "G8Q2": {
        "question_number": "TIMSS-2019-8-M02",
        "domain": "algebra",
        "description": "Linear equations and expressions",
        "image_path": "pics/grade8_q2.png"
    },
    "G8Q3": {
        "question_number": "TIMSS-2019-8-M03",
        "domain": "geometry_measurement",
        "description": "Geometric properties and measurement",
        "image_path": "pics/grade8_q3.png"
    },
    "G8Q4": {
        "question_number": "TIMSS-2019-8-M04",
        "domain": "data_probability",
        "description": "Data analysis and probability",
        "image_path": "pics/grade8_q4.png"
    }
}


def get_question(question_id: str) -> dict:
    """
    Get a specific question.
    
    Args:
        question_id: Question identifier (e.g., "G4Q1", "G8Q3")
        
    Returns:
        Dictionary containing question data
    """
    all_questions = {**GRADE4_QUESTIONS, **GRADE8_QUESTIONS}
    return all_questions.get(question_id, {})


def get_questions_by_grade(grade: int) -> dict:
    """
    Get all questions for a specific grade.
    
    Args:
        grade: Grade level (4 or 8)
        
    Returns:
        Dictionary of questions for the grade
    """
    if grade == 4:
        return GRADE4_QUESTIONS.copy()
    elif grade == 8:
        return GRADE8_QUESTIONS.copy()
    else:
        return {}


def get_questions_by_domain(domain: str) -> dict:
    """
    Get all questions for a specific domain.
    
    Args:
        domain: Mathematics domain
        
    Returns:
        Dictionary of questions for the domain
    """
    all_questions = {**GRADE4_QUESTIONS, **GRADE8_QUESTIONS}
    return {
        k: v for k, v in all_questions.items()
        if v.get("domain") == domain
    }
