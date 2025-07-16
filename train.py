import os, datetime
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from env.airsim_env import AirSimDroneEnv

# -------- logging folder (re‑open = append) ----------
run_id  = datetime.datetime.now().strftime("%H%M%S-%Y%m%d")
log_dir = os.path.join("logs", run_id)
os.makedirs(log_dir, exist_ok=True)

# -------- env + model ----------
env   = AirSimDroneEnv()
model = PPO("MlpPolicy", env,
            n_steps=1024,
            batch_size=64,
            gamma=0.99,
            learning_rate=3e-4,
            verbose=1,
            tensorboard_log=log_dir)

# -------- checkpoint callback -------------
ckpt_cb = CheckpointCallback(
    save_freq=1024,                  # every 1k steps
    save_path="saved_models",
    name_prefix="ppo_airsim"
)

# -------- start/continue training ----------
try:
    model.learn(
        total_timesteps=10_000,      # or 25_000 or 100_000
        callback=ckpt_cb
    )
except KeyboardInterrupt:
    print("\n⏹️  Training interrupted by user (Ctrl+C). "
          "Latest weights are in saved_models/")

model.save("saved_models/ppo_airsim_final")
print("✔  Final model saved.")
