# serve.py  – Flask back‑end that loads the trained model
from flask import Flask, request, jsonify
from stable_baselines3 import PPO
from env.airsim_env import AirSimDroneEnv
import numpy as np

app = Flask(__name__)
env   = AirSimDroneEnv()
model = PPO.load("saved_models/ppo_airsim_final", env=env)

@app.route("/fly", methods=["POST"])
def fly():
    data   = request.get_json(force=True)
    start  = np.array(data["start"], dtype=float)
    goal   = np.array(data["goal"],  dtype=float)

    # force the goal in the env
    obs, _ = env.reset()
    env.goal = goal
    env.client.moveToPositionAsync(*start, velocity=2).join()  # place drone
    obs = env._get_obs() 

    traj = [obs[:3].tolist()]          # ← NEW: record first position
    done = False
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, _, done, _, _ = env.step(action)
        traj.append(obs[:3].tolist())

    return jsonify({"trajectory": traj, "status": "done"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
