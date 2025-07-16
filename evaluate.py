from stable_baselines3 import PPO
from env.airsim_env import AirSimDroneEnv

env   = AirSimDroneEnv()
model = PPO.load("saved_models/ppo_airsim_final.zip", env=env)

obs, _ = env.reset()
done   = False
while not done:
    action, _ = model.predict(obs, deterministic=True)  # deterministic = no exploration
    obs, reward, done, _, info = env.step(action)
    # optional debug
    print(f"dist={info['distance']:.1f}, globalColl={info['global_collision_count']}")
env.close()
