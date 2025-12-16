# Adaptive LLMs Benchmark

A benchmark for evaluating Vision Language Models on adaptive learning tasks using TIMSS mathematics questions with learner-specific prompts.

## Installation

```bash
pip install -r requirements.txt
```

## Setup

Create a `.env` file in the project root with your API keys:

```env
OPENAI_API_KEY=your_openai_key
Huggingface_API_KEY=your_huggingface_token
```

## Project Structure

```
.
├── main.py              # Main evaluation script
├── run_benchmark.py     # Alternative benchmark runner
├── config.py           # Configuration settings
├── data/               # Question data
├── inference/          # Model inference modules
├── prompts/            # Prompt templates and configurations
└── outputs/            # Evaluation results
```

## Usage

### Basic Usage

Run a single evaluation:

```bash
python main.py --model <model_name> --profile <profile> --question <question_id> --group <group>
```
**Example:**
```bash
python main.py --model gpt-4o --profile profile_1 --question G4Q1 --group 4
```

### Multiple Evaluations

Evaluate multiple profiles, questions, or groups:

```bash
# Multiple profiles
python main.py --model gpt-4o --profile profile_1 profile_2 --question G4Q1 --group 4

# Multiple questions
python main.py --model gpt-4o --profile profile_1 --question G4Q1 G4Q2 --group 4

# Multiple groups
python main.py --model gpt-4o --profile profile_1 --question G4Q1 --group 1 2 3 4
```

### Full Evaluation

Run evaluation across all models, profiles, and questions:

```bash
python main.py --full
```

## Learner Profiles

- `profile_1`: Grade 4, high confidence, high TIMSS score (615)
- `profile_2`: Grade 4, low confidence, low TIMSS score (390)
- `profile_3`: Grade 4, confident, medium TIMSS score (550)
- `profile_4`: Grade 8, high confidence, high TIMSS score (625)
- `profile_5`: Grade 8, low confidence, low TIMSS score (400)
- `profile_6`: Grade 8, confident, medium TIMSS score (575)

## Questions

**Grade 4 Questions**: `G4Q1`, `G4Q2`, `G4Q3`, `G4Q4`, `G4Q5`

**Grade 8 Questions**: `G8Q1`, `G8Q2`, `G8Q3`, `G8Q4`, `G8Q5`

## Prompt Groups

- **Group 1**: Image only, no text prompts
- **Group 2**: User prompt only, no system prompt
- **Group 3**: System prompt (without TIMSS context) + User prompt
- **Group 4**: Full system prompt (with TIMSS context) + User prompt

## Output

Results are saved to the `outputs/` directory (configurable with `--output`). Each evaluation generates a JSON file named:

```
{group}_{model_name}_{profile}_{question_id}.json
```

The output includes:
- Model response
- Learner profile configuration
- Question data
- Prompts used (for groups 2-4)
- Metadata (timestamps, model info, etc.)

