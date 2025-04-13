import os
import pickle

from engine.world import World, BACKUP_FILE

os.makedirs(os.path.dirname(BACKUP_FILE), exist_ok=True)

try:
    with open(BACKUP_FILE, "rb") as file:
        world: World = pickle.load(file)
    print("World state loaded from backup.")
except FileNotFoundError:
    print("No backup file found, starting with a new world.")
    world = World()
    print("World initialized.")
except Exception as e:
    print(f"Error loading world state: {e}")
