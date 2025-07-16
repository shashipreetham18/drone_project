🛸 Drone Navigation using Reinforcement Learning + AirSim + Next.js
This project demonstrates how to train and deploy a drone navigation agent using Proximal Policy Optimization (PPO) in the AirSim simulator, with a simple Next.js + Flask frontend to interact and test the model.

🚀 Features
🧠 PPO-based Reinforcement Learning (Stable-Baselines3)

🌍 AirSim simulator (Unreal Engine based)

🌐 Next.js frontend + Flask backend API

📊 Visual control inputs for live testing

📦 Folder Structure

```bash
drone_project/
├── env/                   # Custom AirSim environment wrapper
├── saved_models/          # Trained PPO models
├── train.py               # Training script
├── evaluate.py            # Evaluation script
├── resume.py              # Resume training from checkpoint
├── serve.py               # Flask API server (for model inference)
├── requirements.txt       # Python dependencies
├── web/                   # Next.js frontend
│   ├── pages/
│   │   ├── index.js       # Main UI
│   │   └── api/fly.js     # API proxy to Flask server
│   ├── .env.local         # Environment variables (optional)
├── .gitignore
└── README.md
```
⚙️ Setup & Installation
Python (Backend - Flask + AirSim)

Step 1: Clone the repository
git clone https://github.com/shashipreetham18/drone_project.git
cd drone_project

Step 2: Set up virtual environment
python -m venv venv
venv\Scripts\activate (On Windows)
OR
source venv/bin/activate (On Linux/Mac)

Step 3: Install Python dependencies
pip install -r requirements.txt

Step 4: Launch AirSim
Download and open AirSimNH.exe (City or Neighborhood environment).
Make sure the simulator is running before starting the server.

Step 5: Run the backend Flask server
python serve.py

The Flask server runs at: http://127.0.0.1:5000/fly

🌐 Web Frontend (Next.js)
Step 1: Install frontend dependencies
cd web
npm install

Step 2: Run the development server
npm run dev

Then open http://localhost:3000 in your browser.

🧠 How the Model Works
Environment: AirSim 3D simulator

Action Space: 5–7 discrete drone actions

Observation Space: Position + Goal vector

Algorithm: PPO (Proximal Policy Optimization)

🧪 Example Use Flow
Start the Flask server

Open the Next.js frontend

Select position + goal

Model predicts action via Flask

Output shown in UI / simulator

🛠 To Do
 Visual path overlay (map or image)

 Host backend (if needed externally)

 Add collision detection & feedback

 Add support for real drone hardware (future scope)

📚 Resources
AirSim GitHub: https://github.com/microsoft/AirSim

Stable-Baselines3: https://stable-baselines3.readthedocs.io/

PPO Paper (OpenAI): https://arxiv.org/abs/1707.06347

🤝 Maintainer
Shashi Preetham (https://github.com/shashipreetham18)

🏁 License
MIT License
