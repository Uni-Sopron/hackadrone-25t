import os
import pickle

from engine.world import World, BACKUP_DIR

os.makedirs(BACKUP_DIR, exist_ok=True)

backups = [f for f in os.scandir(BACKUP_DIR)]
if backups:
    backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    print(f"Loading world state from backup: {backups[0].name}")
    with open(backups[0], "rb") as file:
        world: World = pickle.load(file)
    world.migrate()
    print("World state loaded from backup.")
else:
    print("No backup file found, starting with a new world.")
    world = World()
    print("World initialized.")
