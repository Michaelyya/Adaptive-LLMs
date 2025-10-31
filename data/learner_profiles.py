
TIMSS_BENCHMARKS = {
    "grade4": {
        "advanced": 625,
        "high": 550,
        "intermediate": 475,
        "low": 400
    },
    "grade8": {
        "advanced": 625,
        "high": 550,
        "intermediate": 475,
        "low": 400
    }
}

LEARNER_PROFILES = {
    # Grade 4 Learners
    "grade4_high": {
        "grade": 4,
        "performance_level": "high",
        "learner_background": {
            "grade": 4,
            "early_education": "enrolled",
            "language": "primary_language"
        },
        "learner_behavior": {
            "math_attitude": "high_positive",
            "confidence": "high",
            "engagement": "high"
        },
        "knowledge_level": {
            "domains": ["number", "measurement", "data"],
            "timss_score": 580,  # Above intermediate benchmark
            "benchmark": "intermediate_to_high",
            "topics_taught": [
                "Whole numbers",
                "Fractions and decimals",
                "Measurement units",
                "Data representation"
            ]
        }
    },
    
    "grade4_middle": {
        "grade": 4,
        "performance_level": "middle",
        "learner_background": {
            "grade": 4,
            "early_education": "enrolled",
            "language": "primary_language"
        },
        "learner_behavior": {
            "math_attitude": "moderate",
            "confidence": "moderate",
            "engagement": "moderate"
        },
        "knowledge_level": {
            "domains": ["number", "measurement", "data"],
            "timss_score": 490,  # Near intermediate benchmark
            "benchmark": "intermediate",
            "topics_taught": [
                "Whole numbers",
                "Basic fractions",
                "Basic measurement",
                "Simple data reading"
            ]
        }
    },
    
    "grade4_low": {
        "grade": 4,
        "performance_level": "low",
        "learner_background": {
            "grade": 4,
            "early_education": "mixed",
            "language": "primary_language"
        },
        "learner_behavior": {
            "math_attitude": "low",
            "confidence": "low",
            "engagement": "low"
        },
        "knowledge_level": {
            "domains": ["number", "measurement", "data"],
            "timss_score": 430,  # Below intermediate benchmark
            "benchmark": "low_to_intermediate",
            "topics_taught": [
                "Counting and basic operations",
                "Simple measurements",
                "Basic data reading"
            ]
        }
    },
    
    # Grade 8 Learners
    "grade8_high": {
        "grade": 8,
        "performance_level": "high",
        "learner_background": {
            "grade": 8,
            "early_education": "enrolled",
            "language": "primary_language"
        },
        "learner_behavior": {
            "math_attitude": "high_positive",
            "confidence": "high",
            "engagement": "high"
        },
        "knowledge_level": {
            "domains": ["number", "algebra", "geometry_measurement", "data_probability"],
            "timss_score": 590,  # Above intermediate benchmark
            "benchmark": "intermediate_to_high",
            "topics_taught": [
                "Rational numbers",
                "Linear equations",
                "Geometric shapes and properties",
                "Data analysis and probability"
            ]
        }
    },
    
    "grade8_middle": {
        "grade": 8,
        "performance_level": "middle",
        "learner_background": {
            "grade": 8,
            "early_education": "enrolled",
            "language": "primary_language"
        },
        "learner_behavior": {
            "math_attitude": "moderate",
            "confidence": "moderate",
            "engagement": "moderate"
        },
        "knowledge_level": {
            "domains": ["number", "algebra", "geometry_measurement", "data_probability"],
            "timss_score": 500,  # Near intermediate benchmark
            "benchmark": "intermediate",
            "topics_taught": [
                "Rational numbers",
                "Basic algebra",
                "Basic geometry",
                "Data reading and basic probability"
            ]
        }
    },
    
    "grade8_low": {
        "grade": 8,
        "performance_level": "low",
        "learner_background": {
            "grade": 8,
            "early_education": "mixed",
            "language": "primary_language"
        },
        "learner_behavior": {
            "math_attitude": "low",
            "confidence": "low",
            "engagement": "low"
        },
        "knowledge_level": {
            "domains": ["number", "algebra", "geometry_measurement", "data_probability"],
            "timss_score": 440, 
            "benchmark": "low_to_intermediate",
            "topics_taught": [
                "Whole numbers",
                "Basic number operations",
                "Simple geometric concepts",
                "Basic data reading"
            ]
        }
    }
}


def get_learner_profile(profile_id: str) -> dict:
    return LEARNER_PROFILES.get(profile_id, {})


def get_all_profiles() -> dict:
    return LEARNER_PROFILES.copy()


def get_profiles_by_grade(grade: int) -> dict:
    return {
        k: v for k, v in LEARNER_PROFILES.items()
        if v.get("grade") == grade
    }
