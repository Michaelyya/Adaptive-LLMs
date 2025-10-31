# Adaptive Learning LLM Benchmark

A comprehensive benchmark for evaluating LLM-based adaptive learning systems in mathematics education using TIMSS 2019 data.

## Overview

This project implements a learner model-based benchmark grounded in adaptive learning research to evaluate how well different Large Language Models (LLMs) can provide personalized mathematics instruction to learners with varying academic backgrounds.

## Research Framework

- **Adaptive Learning Framework**: Based on Shute & Towle (2018)
- **Learner Model Components**: Background, Behavior, Knowledge Level
- **Data Source**: TIMSS 2019 Mathematics Questions
- **Target Domains**: 
  - Grade 4: Number, Measurement, Data
  - Grade 8: Number, Algebra, Geometry/Measurement, Data/Probability

## Project Structure

```
.
├── inference/          # Model inference modules
│   ├── __init__.py
│   ├── base_inference.py
│   ├── llama_inference.py
│   └── openai_inference.py
├── prompts/            # Prompts and parameters
│   ├── __init__.py
│   ├── system_prompts.py
│   ├── user_prompts.py
│   └── parameters.py
├── data/              # Learner profiles and question data
│   ├── learner_profiles.py
│   └── question_data.py
├── pics/              # TIMSS question images
├── outputs/           # Model outputs and results
├── main.py           # Main orchestration script
├── config.py         # Configuration file
└── README.md
```

## Models Evaluated

### Vision-Language Models (VLLMs)
- **Llama**: Llama-3.2-11B-Vision-Instruct, Llama-3.2-90B-Vision, Llama-4-Scout-17B-16E-Instruct
- **OpenAI**: GPT-4o, GPT-5, O1

## Learner Profiles

Six learner profiles based on TIMSS 2019 data:
- Grade 4: High, Middle, Low performance
- Grade 8: High, Middle, Low performance

Each profile includes:
- Background (grade, language, early education)
- Behavior (math attitude, confidence, engagement)
- Knowledge level (TIMSS scores, benchmarks, topics)

## Setup

### Prerequisites
```bash
pip install transformers torch openai
pip install transformers[vision]  # For vision models
```

### Environment Variables
```bash
export OPENAI_API_KEY="your-openai-key"
export HUGGINGFACE_TOKEN="your-hf-token"
```

### Download TIMSS Images
Place TIMSS question images in the `pics/` directory with appropriate naming:
- `pics/grade4_q1.png`
- `pics/grade4_q2.png`
- etc.

## Usage

### Full Evaluation
```bash
python main.py --full --output outputs
```

### Specific Evaluation
```bash
python main.py \
    --model "meta-llama/Llama-3.2-11B-Vision-Instruct" \
    --profile "grade4_high" \
    --question "G4Q1" \
    --output outputs
```

## Output Format

Results are saved as JSON files with:
- Model configuration
- Learner profile data
- Question data
- Prompts used
- Model response
- Metadata (tokens, timing, etc.

## Citation

If you use this benchmark in your research, please cite:
```
Adaptive Learning LLM Benchmark: Evaluating Personalization in Mathematics Education
[Add your publication details]
```

## License

[Specify license]

## Contact

[Add contact information]
