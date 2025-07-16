import os, glob
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from env.airsim_env import AirSimDroneEnv

ckpts = sorted(glob.glob("saved_models/ppo_airsim_*_steps.zip"))
latest_ckpt = ckpts[-1] if ckpts else None
print("Latest checkpoint:", latest_ckpt or "None starting fresh")
env = AirSimDroneEnv()

if latest_ckpt:
    model = PPO.load(latest_ckpt, env=env, verbose=1)
else:
    model = PPO("MlpPolicy", env, verbose=1)
ckpt_cb = CheckpointCallback(save_freq=1024,
                             save_path="saved_models",
                             name_prefix="ppo_airsim")
model.learn(total_timesteps=10_000,
            reset_num_timesteps=False, 
            callback=ckpt_cb)

model.save("saved_models/ppo_airsim_final")
print("Training done. Model saved as saved_models/ppo_airsim_final.zip")
