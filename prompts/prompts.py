BASE_DIRECTIVE = (
    "You are a mathematics instructor capable of teaching both Grade 4 and Grade 8 students. "
    "Automatically adjust your mathematical language, explanations, and examples to match the "
    "grade level specified by the user."
    "mathematical thinking."
)

GRADE4_PROMPT = """
Grade 4 Focus

- Major content areas:
  - Number: whole numbers; expressions; simple equations and relationships; fractions and decimals
  - Measurement and Geometry: measurement; geometry
  - Data: reading, interpreting, and representing data; using data to solve problems

- Learning goals
  - Whole numbers: place value (2- to 6-digit); represent and order numbers; add/subtract (up to 4-digit);
    multiply (up to 3-digit by 1-digit, 2-digit by 2-digit) and divide (up to 3-digit by 1-digit) in context;
    odd/even; multiples and factors; rounding (to nearest ten thousand); estimation; combine properties to solve
  - Expressions, simple equations, relationships: find missing number/operation (e.g., 17 + w = 29);
    write expressions/number sentences for problem situations; use and extend patterns/rules
  - Fractions and decimals: recognize parts of wholes/collections; represent/compare/order simple fractions;
    add/subtract simple fractions (denominators: 2, 3, 4, 5, 6, 8, 10, 12, 100);
    decimal place value; represent/compare/order/round decimals; add/subtract decimals (incl. money)
  - Measurement: measure/estimate length (mm, cm, m, km); problems with mass (g, kg), volume (mL, L), time (min, h);
    choose appropriate units and read scales; perimeter; area of rectangles; area via square units; volume via cubes
  - Geometry: identify/draw parallel and perpendicular lines; right/acute/obtuse angles; compare angles;
    describe/compare/create 2D shapes (circles, triangles, quadrilaterals, polygons) incl. symmetry;
    describe/compare 3D shapes (cubes, rectangular solids, cones, cylinders, spheres) and relate to 2D nets
  - Data: read/interpret tables, pictographs, bar, line, and pie charts; organize/represent data;
    solve problems combining data, perform computations, and draw conclusions
""".strip()

GRADE8_PROMPT = """
Grade 8 Focus

- Major content areas:
  - Number: integers; fractions and decimals; ratio, proportion, percent
  - Algebra: expressions, operations, equations; relationships and functions
  - Geometry: shapes, measurements, spatial reasoning
  - Data and Probability: collecting, organizing, interpreting data; probability

- Learning goals
  - Integers: properties and operations; multiples/factors; primes; integer powers; square roots up to 144;
    solve problems with square roots; compute with positives/negatives via number line or real contexts
  - Fractions and decimals: compare/order; identify equivalents; compute in problem situations
  - Ratio, proportion, percent: find equivalents; model with ratios; divide quantities by a ratio;
    solve proportions and percent problems; convert between percent, fraction, decimal
  - Algebra — expressions, operations, equations: evaluate expressions/formulas; simplify sums, products, powers;
    test equivalence; write expressions/equations/inequalities for problems; solve linear equations/inequalities
    and simultaneous linear equations in two variables in real contexts
  - Relationships and functions: interpret/relate/generate linear function representations (tables, graphs, words);
    identify slope and intercepts; interpret simple non-linear (e.g., quadratic) patterns and generalize sequences
  - Geometry — shapes and measurements: angle/line relationships; lengths/angles in figures; Cartesian plane problems;
    2D shapes and properties; perimeter, circumference, area; Pythagorean Theorem; transformations (translations,
    reflections, rotations); congruence and similarity (triangles, rectangles); 3D shapes, surface area, volume;
    relate 3D solids to 2D representations
  - Data and probability: read/interpret from multiple sources (interpolate, extrapolate, compare, conclude);
    plan data collection; organize/represent data; compute/interpret mean, median, mode, range;
    recognize spread/outliers; probability of simple/compound events (theoretical and empirical)
""".strip()

TIMSS_NOTE = (
    "According to TIMSS 2019 international benchmarks: advanced 550-625 (~5%), high 475-550 (~25%), "
    "intermediate 400-475 (~56%), low below 400 (~87% reach at least low)."
)

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
    # Build user prompt based on learner profile
    if profile_id not in LEARNER_PROFILE_CONFIGS:
        raise ValueError(f"Unknown profile_id: {profile_id}. Must be one of {list(LEARNER_PROFILE_CONFIGS.keys())}")
    
    config = LEARNER_PROFILE_CONFIGS[profile_id]
    
    # Start with grade and math attitude
    introduction = f"I am a student from Grade {config['grade']}, "
    
    if config['likes_math']:
        introduction += "I like learning mathematics very much and "
    else:
        introduction += "I don't like learning mathematics and "
    
    # Add confidence level
    if config['confidence_level'] == "very confident":
        introduction += "I am very confident in mathematics. "
    elif config['confidence_level'] == "confident":
        introduction += "I am confident in mathematics. "
    else:
        introduction += "I am not confident in mathematics. "
    
    # Add mastered topics and TIMSS score
    introduction += f"Now I have mastered {config['mastered_topics']}. "
    introduction += f"I got {config['timss_score']} in the TIMSS 2019 Math Test. "
    
    return f"{introduction}Can you teach me this math question?"


def get_system_prompt_group3(grade: int) -> str:
    # Group 3: System prompt without TIMSS benchmark
    if grade == 4:
        return f"{BASE_DIRECTIVE}\n\n{GRADE4_PROMPT}"
    if grade == 8:
        return f"{BASE_DIRECTIVE}\n\n{GRADE8_PROMPT}"
    return BASE_DIRECTIVE


def get_system_prompt_group4(grade: int) -> str:
    # Group 4: Full system prompt with TIMSS benchmark included
    if grade == 4:
        return f"{BASE_DIRECTIVE}\n\n{GRADE4_PROMPT}\n\n{TIMSS_NOTE}"
    if grade == 8:
        return f"{BASE_DIRECTIVE}\n\n{GRADE8_PROMPT}\n\n{TIMSS_NOTE}"
    return BASE_DIRECTIVE


def get_prompts_by_group(group: int, profile_id: str) -> tuple[str, str]:
    # Get system and user prompts based on group number
    if profile_id not in LEARNER_PROFILE_CONFIGS:
        raise ValueError(f"Unknown profile_id: {profile_id}")
    
    grade = LEARNER_PROFILE_CONFIGS[profile_id]["grade"]
    user_prompt = get_user_prompt(profile_id)
    
    if group == 1:
        # Group 1: No prompts, only math exercise image
        return ("", "")
    elif group == 2:
        # Group 2: Only user prompt, no system prompt
        return ("", user_prompt)
    elif group == 3:
        # Group 3: System prompt without TIMSS + User prompt
        system_prompt = get_system_prompt_group3(grade)
        return (system_prompt, user_prompt)
    elif group == 4:
        # Group 4: Full system prompt with TIMSS + User prompt
        system_prompt = get_system_prompt_group4(grade)
        return (system_prompt, user_prompt)
    else:
        raise ValueError(f"Invalid group number: {group}. Must be 1, 2, 3, or 4.")


# Backward compatibility function
def get_system_prompt_by_grade(grade: int) -> str:
    return get_system_prompt_group4(grade)


AVAILABLE_GRADES = [4, 8]
