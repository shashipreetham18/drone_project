import time
import numpy as np
import airsim
import gymnasium as gym
from gymnasium import spaces


class AirSimDroneEnv(gym.Env):
    def __init__(self,
                 ip: str = "127.0.0.1",
                 port: int = 41451,
                 goal_radius: float = 1.0):
        super().__init__()

        # --- AirSim connection ---
        self.client = airsim.MultirotorClient(ip=ip, port=port)
        self.client.confirmConnection()

        # --- spaces ---
        high = np.array([150, 150, 20, 10, 10, 10, 300], np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)
        self.action_space      = spaces.Box(-1.0, 1.0, (3,), dtype=np.float32)

        # --- config ---
        self.dt           = 0.10        # 10 Hz control loop
        self.goal_radius  = goal_radius
        self.max_steps    = 300
        self._grace_steps = 2

        # ---------- NEW: global collision watchdog ----------
        self.collision_reset_threshold = 50   # ⇐ change here if you want 100, etc.
        self.global_collision_count    = 0
        # ----------------------------------------------------

        self.state = None
        self._step_count = 0


    # ------------------------------------------------------
    def _get_obs(self):
        kin  = self.client.getMultirotorState().kinematics_estimated
        pos  = kin.position
        vel  = kin.linear_velocity
        dist = np.linalg.norm(np.array([pos.x_val, pos.y_val, pos.z_val]) - self.goal)
        return np.array([pos.x_val, pos.y_val, pos.z_val,
                         vel.x_val, vel.y_val, vel.z_val,
                         dist], np.float32)

    # ------------------------------------------------------
    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)

        # random start/goal
        sx, sy = np.random.uniform(-120, 120, 2)
        gx, gy = np.random.uniform(-120, 120, 2)
        alt    = -8.0
        self.goal = np.array([gx, gy, alt], np.float32)

        # full simulator reset
        self.client.reset()
        time.sleep(0.2)
        self.client.enableApiControl(True)
        self.client.armDisarm(True)
        self.client.takeoffAsync().join()
        self.client.moveToPositionAsync(0, 0, -15, 3).join()
        self.client.moveToPositionAsync(float(sx), float(sy), -15, 4).join()
        self.client.moveToPositionAsync(float(sx), float(sy), alt, 3).join()

        # clear counters
        self._step_count            = 0
        self.global_collision_count = 0        # ### NEW ###
        return self._get_obs(), {}


    # ------------------------------------------------------
    def step(self, action):
        vx, vy, vz = [float(a) * 4.0 for a in np.clip(action, -1.0, 1.0)]
        self.client.moveByVelocityAsync(
            vx, vy, vz, self.dt,
            drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom,
            yaw_mode=airsim.YawMode(False, 0)
        )
        time.sleep(self.dt)

        self._step_count += 1
        obs  = self._get_obs()
        dist = obs[6]

        # ----- collision check -----
        collision = False
        ci = self.client.simGetCollisionInfo()
        if hasattr(ci, "has_collided"):
            collision = ci.has_collided
        if self._step_count <= self._grace_steps:
            collision = False

        # ----- reward / termination -----
        reward, terminated = -0.05 * dist - 0.01, False
        if dist < self.goal_radius:
            reward += 100; terminated = True
        elif collision:
            reward -= 50;  terminated = True
        elif self._step_count >= self.max_steps:
            terminated = True

        # ---------- NEW: global collision watchdog ----------
        if collision:
            self.global_collision_count += 1
            if self.global_collision_count >= self.collision_reset_threshold:
                print("=== Hard reset triggered after "
                      f"{self.global_collision_count} collisions ===")
                self.client.reset()              # free the stuck drone
                self.global_collision_count = 0  # restart the tally
                terminated = True                # force episode end
        # ----------------------------------------------------

        info = {
            "distance": dist,
            "global_collision_count": self.global_collision_count  # debug
        }
        return obs, reward, terminated, False, info


    # ------------------------------------------------------
    def close(self):
        self.client.armDisarm(False)
        self.client.enableApiControl(False)
