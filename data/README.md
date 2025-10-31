# Data Directory

This directory contains learner profile data and question data based on TIMSS 2019.

## Files

### learner_profiles.py
Contains learner profile definitions based on adaptive learning framework:
- **Learner Background**: Grade, language, early education, social-emotional learning
- **Learner Behavior**: Math attitude, confidence, engagement
- **Knowledge Level**: TIMSS scores, benchmarks, taught topics

### question_data.py
Contains TIMSS 2019 mathematics question metadata:
- Question numbers
- Domains (number, algebra, geometry, measurement, data, probability)
- Descriptions
- Image file paths

## Learner Profiles

Six profiles are defined:
- **Grade 4**: High, Middle, Low performance
- **Grade 8**: High, Middle, Low performance

## TIMSS Benchmarks

Grade 4:
- Low: Below 400
- Intermediate: 400-500
- High: 500-550
- Advanced: Above 625

Grade 8:
- Low: Below 400
- Intermediate: 400-500
- High: 500-550
- Advanced: Above 625

## Source Data

Original TIMSS data available at:
https://timssandpirls.bc.edu/timss2019/
