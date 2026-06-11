# Program Analytics & AI Mentor Insight API

A Django REST backend for ingesting learner program data, detecting dataset structure, and generating AI-assisted mentor insights for software engineering cohorts.

## Features

- Upload survey and learner activity CSV files
- Store dataset metadata including filename, row count, column count, cohort, and program
- Prevent duplicate uploads using file hashing
- Detect semantic column types such as NPS, CSAT, email, assignment score, learner status, activity, and retention signals
- Generate AI-assisted mentor recommendations from uploaded datasets
- Provide fallback rule-based insights when the AI provider is unavailable
- Retrieve datasets, rows, columns, and generated insights through REST APIs

## Tech Stack

- Python
- Django
- Django REST Framework
- Pandas
- SQLite
- OpenAI API
- Python dotenv

## API Endpoints

### Upload Dataset

POST /api/analytics/upload/<cohort_id>/<dataset_type>/

Form-data:

file: CSV file
program: backend

Allowed dataset types:

survey
learner_activities

Allowed programs:

frontend
backend
prodev_frontend
prodev_backend

### List Datasets

GET /api/analytics/datasets/

### Dataset Detail

GET /api/analytics/datasets/<dataset_id>/

### Dataset Columns

GET /api/analytics/datasets/<dataset_id>/columns/

### Dataset Rows

GET /api/analytics/datasets/<dataset_id>/rows/

### Generate AI Insight

POST /api/analytics/datasets/<dataset_id>/ai-insights/

### Dataset Insights

GET /api/analytics/datasets/<dataset_id>/insights/

## Environment Variables

DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4.1-mini

## Local Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver