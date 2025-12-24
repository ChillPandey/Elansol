Real-Time Event Monitoring Dashboard

A simple and practical real-time event tracking system built with Python, Streamlit, and SQLite.
This project demonstrates how events can be sent through an API, stored in a database, and visualized live on a dashboard.

⸻

✨ Features
	•	REST API for receiving events
	•	SQLite database for persistent storage
	•	Live dashboard using Streamlit
	•	Auto-refreshing event table
	•	Clean and minimal architecture

⚙️ Setup Instructions

1. Clone the repository
   git clone https://github.com/ChillPandey/Elansol
   cd elansol
2. Create a virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate #Windows: venv\Scripts\activate
3. Install dependencies
   pip install -r requirements.txt

▶️ Running the Project

Start the API Server
python api_server.py

Launch the Dashboard
streamlit run app.py
Open the displayed URL (usually http://localhost:8501) in your browser.

📡 Sending Events (Example)

You can send events using curl, Postman, or any HTTP client.
curl -X POST http://localhost:5000/event \
-H "Content-Type: application/json" \
-d '{"event_type": "temperature", "value": 30}'
The event will be stored and instantly reflected on the dashboard.

🧠 How It Works
	1.	Events are sent to the API
	2.	API stores events in SQLite
	3.	Streamlit reads and displays data in real time

This keeps the system simple, fast, and easy to understand.

🛠 Tech Stack
	•	Python
	•	Streamlit
	•	SQLite
	•	REST API
	•	Pandas
