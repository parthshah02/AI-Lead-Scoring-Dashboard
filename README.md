# Lead Scoring Dashboard

A web-based dashboard that predicts lead intent using machine learning and LLM-inspired re-ranking.

## Project Structure
```
cleardeal/
├── frontend/         # React frontend application
│   ├── public/      # Static files
│   └── src/         # Source code
├── backend/         # FastAPI backend
│   └── model/       # Trained model
├── model/          # Model training code
└── data/          # Dataset and model artifacts
```

## Setup Instructions

### Backend Setup
1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Start the FastAPI server:
```bash
python main.py
```

### Frontend Setup
1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the React development server:
```bash
npm start
```

The application will be available at `http://localhost:3000` and the backend API at `http://localhost:8000`.

## Features
- Lead scoring using machine learning
- LLM-inspired re-ranking
- Responsive dashboard UI
- Real-time scoring
- Lead data visualization
- Input validation and error handling
- Consent management

## Data Processing
The application uses synthetic data for lead scoring and does not collect or process real PII. All data is stored in memory and is cleared when the server restarts.

## License
MIT
