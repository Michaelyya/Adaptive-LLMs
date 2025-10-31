# Outputs Directory

This directory contains all evaluation results from the adaptive learning benchmark.

## Output File Structure

Each evaluation produces a JSON file with the following structure:

```
{
  "timestamp": "2024-01-01T12:00:00",
  "model": "model-name",
  "model_type": "llama|openai",
  "learner_profile": "grade4_high",
  "learner_data": {...},
  "question_id": "G4Q1",
  "question_data": {...},
  "system_prompt": "...",
  "user_prompt": "...",
  "generation_params": {...},
  "response": "model response text",
  "metadata": {
    "tokens_used": 123,
    ...
  }
}
```

## Summary File

After running evaluations, a `summary.json` file will be created containing:
- Total number of evaluations
- List of all completed evaluations
- Timestamp

## File Naming Convention

Files are named as: `{model}_{learner_profile}_{question_id}_{timestamp}.json`

For example: `gpt-4o_grade4_high_G4Q1_20240101_120000.json`
