# Developer Onboarding Guide

Welcome to the AI Decision Engine module. This guide covers how to set up the development environment, execute the test suite, and run the simulator.

## 1. Environment Setup

Ensure you are using **Python 3.10+**.

```bash
# Clone the repository and navigate into the directory
cd Decision_Engine

# Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Configuration
Copy the `.env.example` file to create your local `.env`.
```bash
cp configs/.env.example configs/.env
```

## 3. Running the Server
The application is built on FastAPI. Run the development server using `uvicorn`.
```bash
# Must be executed from the project root
uvicorn app.main:app --reload --port 8000
```
Visit `http://127.0.0.1:8000/docs` to test the API via the Swagger UI.

## 4. Running the Test Suite
The project maintains a rigorous, 59-test validation suite covering unit components, integration paths, and edge cases.
```bash
# Run all tests with short traceback
python -m pytest tests/ -v --tb=short
```

## 5. Running the Simulator
The simulation engine tests the system against 6 distinct AI personas (e.g., Fatigued, Inconsistent, Nervous) without requiring actual network requests.
```bash
# Run all personas
python simulations/runner.py --persona all

# Run a specific persona
python simulations/runner.py --persona WeakCandidate
```
