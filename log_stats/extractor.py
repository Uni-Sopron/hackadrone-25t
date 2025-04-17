import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
from datetime import datetime
import json
import os
import pandas as pd

TEAMS = ["Hubertus", "FoxDrone", "Karesz", "RoadRunnerExpress"]
DRONE_STATES = ["moving", "charging", "idle", "swapping", "dead"]
OPERATIONAL_DRONE_STATES = ["moving", "idle", "charging"]
SIZE = (16,9)

def get_admin_data(admin_log_dir):
    admindata = {}
    for file in os.listdir(admin_log_dir):
        timestamp = datetime.strptime(file, "data_%Y%m%d_%H%M%S.json")
        with open(os.path.join(admin_log_dir,file)) as f:
            admindata[timestamp] = json.load(f)
    return admindata


def score_over_time(admindata, filename):
    df = pd.DataFrame(columns=TEAMS)
    df.index.name = "timestamp"
    for timestamp, data in admindata.items():
        row = {}
        for team in data["teams"]:
            row[team["name"]] = team["score"] 
        df.loc[timestamp] = row
    df.sort_values(by="timestamp", inplace=True)
    df.plot(figsize=SIZE)
    plt.legend(title="Teams")
    plt.gca().set_xlabel("")
    plt.tight_layout()
    plt.savefig(f"{filename}.png")
    df.to_excel(f"{filename}.xlsx", index=False)

def operational_drone_over_time(admindata, filename):
    df = pd.DataFrame(columns=DRONE_STATES)
    df.index.name = "timestamp"
    for timestamp, data in admindata.items():
        count = { state : 0 for state in DRONE_STATES}
        for drone in data["drones"]:
            count[drone["state"]] += 1
        df.loc[timestamp] = count
    df.sort_values(by="timestamp", inplace=True)
    df.plot.area(figsize=SIZE, stacked=True)
    plt.legend(title="Drone States")
    colors = {
        "moving": "green",
        "charging": "orange",
        "idle": "blue",
        "swapping": "gray",
        "dead": "black"
    }
    df.plot.area(figsize=SIZE, stacked=True, color=[colors[state] for state in DRONE_STATES])
    plt.gca().set_xlabel("")
    plt.tight_layout()
    plt.savefig(f"{filename}.png")
    df.to_excel(f"{filename}.xlsx", index=False)

    for team in TEAMS:
        plt.clf()
        df = pd.DataFrame(columns=DRONE_STATES)
        df.index.name = "timestamp"
        for timestamp, data in admindata.items():
            count = { state : 0 for state in DRONE_STATES}
            for drone in data["drones"]:
                if drone["team_id"] == team:
                    count[drone["state"]] += 1
            df.loc[timestamp] = count
        df.sort_values(by="timestamp", inplace=True)
        df.plot.area(figsize=SIZE, stacked=True)
        plt.legend(title="Drone States")
        colors = {
            "moving": "green",
            "charging": "orange",
            "idle": "blue",
            "swapping": "gray",
            "dead": "black"
        }
        df.plot.area(figsize=SIZE, stacked=True, color=[colors[state] for state in DRONE_STATES])
        plt.gca().set_xlabel("")
        plt.title(team)
        plt.tight_layout()
        plt.savefig(f"{filename}_{team}.png")


def prepare_docker_logs(logdir, outputfilename):
    with open(outputfilename, "w") as report:
        for file in os.listdir(logdir):
            if file.endswith(".log"):
                with open(os.path.join(logdir,file)) as f:
                    for line in f:
                        if "WORLD | DELAY |" in line: continue
                        if "| ADD CHARGING STATION |" in line: continue
                        if "'action': 'new_drone'" in line: continue
                        report.write(line)
        

def status_tariff(dockerlogfile, filename, ignore_hours = 0):
    df = pd.DataFrame(columns=[f"{team}-{price}" for team in ["all", *TEAMS] for price in ["free", "paid"]])
    df.index.name = "timestamp"
    free = {}
    paid = {}
    with open(dockerlogfile) as f:
        for line in f:
            if "HUF for: API request" in line:
                timestamp = datetime.strptime(line.split(".")[0], "%Y-%m-%dT%H:%M:%S")
                timestamp = timestamp.replace(second=0, minute=0)
                if timestamp not in free:
                    free[timestamp] = {"all":0, **{team:0 for team in TEAMS}} 
                    paid[timestamp] = {"all":0, **{team:0 for team in TEAMS}} 
                team = line.split("| TARIFF |")[1].split("charged")[0].strip()
                if " 10 HUF" in line: 
                    paid[timestamp]["all"] += 1
                    paid[timestamp][team] += 1
                else: 
                    free[timestamp]["all"] += 1
                    free[timestamp][team] += 1
    for timestamp in free:
        df.loc[timestamp] = { 
            **{f"{team}-free": count for team,count in free[timestamp].items()},
            **{f"{team}-paid": count for team,count in paid[timestamp].items()}
        }
    df.sort_values(by="timestamp", inplace=True)
    for team in ["all", *TEAMS]:
        df[team] = df[f"{team}-free"] + df[f"{team}-paid"]

    df = df[df.index >= df.index[0] + pd.Timedelta(hours=ignore_hours)]

    df[TEAMS].plot(kind='area', stacked=True, figsize=SIZE)
    plt.title("Status requests over time")
    plt.legend()
    plt.gca().set_xlabel("")
    plt.tight_layout()
    plt.savefig(f"{filename}_over_time.png")

    plt.clf() 

    df[[f"{team}-paid" for team in TEAMS]].plot(kind='area', stacked=True, figsize=SIZE)
    plt.title("Paid status requests over time")
    plt.legend()
    plt.gca().set_xlabel("")
    plt.tight_layout()
    plt.savefig(f"{filename}_over_time_paid.png")

    plt.clf() 

    column_sums = df[TEAMS].sum()
    column_sums.plot(kind='pie', figsize=SIZE, autopct=lambda p: f'{p:.1f}%\n({int(p * column_sums.sum() / 100)})')
    
    plt.legend()
    plt.ylabel("")
    plt.title("Sum of Status Requests")
    plt.tight_layout()
    plt.savefig(f"{filename}.png")

    df.to_excel(f"{filename}.xlsx", index=False)
    

def charging_tariff(dockerlogfile, filename, ignore_hours = 0):
    df = pd.DataFrame(columns=[f"{team}-{price}" for team in ["all", *TEAMS] for price in ["free", "paid"]])
    df.index.name = "timestamp"
    free = {}
    paid = {}
    with open(dockerlogfile) as f:
        for line in f:
            if "HUF for: recharging" in line:
                timestamp = datetime.strptime(line.split(".")[0], "%Y-%m-%dT%H:%M:%S")
                timestamp = timestamp.replace(second=0, minute=0)
                if timestamp not in free:
                    free[timestamp] = {"all":0, **{team:0 for team in TEAMS}} 
                    paid[timestamp] = {"all":0, **{team:0 for team in TEAMS}} 
                team = line.split("| TARIFF |")[1].split("charged")[0].strip()
                cost = int(line.split("charged")[1].split("HUF")[0])
                amount = float(line.split("with")[1].split("Wh")[0])
                if cost > 0: 
                    paid[timestamp]["all"] += amount
                    paid[timestamp][team] += amount
                else: 
                    free[timestamp]["all"] += amount
                    free[timestamp][team] += amount
    for timestamp in free:
        df.loc[timestamp] = { 
            **{f"{team}-free": count for team,count in free[timestamp].items()},
            **{f"{team}-paid": count for team,count in paid[timestamp].items()}
        }
    df.sort_values(by="timestamp", inplace=True)
    for team in ["all", *TEAMS]:
        df[team] = df[f"{team}-free"] + df[f"{team}-paid"]

    df = df[df.index >= df.index[0] + pd.Timedelta(hours=ignore_hours)]

    df[TEAMS].plot(kind='area', stacked=True, figsize=SIZE)
    plt.title("Energy from stations over time (Wh)")
    plt.legend()
    plt.gca().set_xlabel("")
    plt.tight_layout()
    plt.savefig(f"{filename}_over_time.png")

    plt.clf() 

    df[[f"{team}-paid" for team in TEAMS]].plot(kind='area', stacked=True, figsize=SIZE)
    plt.title("Paid energy from stations over time (Wh)")
    plt.legend()
    plt.gca().set_xlabel("")
    plt.tight_layout()
    plt.savefig(f"{filename}_over_time_paid.png")

    plt.clf() 

    column_sums = df[TEAMS].sum()
    column_sums.plot(kind='pie', figsize=SIZE, autopct=lambda p: f'{p:.1f}%\n({int(p * column_sums.sum() / 100)} Wh)')
    
    plt.legend()
    plt.ylabel("")
    plt.title("Sum of energy from stations")
    plt.tight_layout()
    plt.savefig(f"{filename}.png")

    df.to_excel(f"{filename}.xlsx", index=False)



def docking_tariff(dockerlogfile, filename, ignore_hours = 0):
    df = pd.DataFrame(columns=[f"{team}-{price}" for team in ["all", *TEAMS] for price in ["free", "paid"]])
    df.index.name = "timestamp"
    free = {}
    paid = {}
    with open(dockerlogfile) as f:
        for line in f:
            if "docking at station" in line:
                timestamp = datetime.strptime(line.split(".")[0], "%Y-%m-%dT%H:%M:%S")
                timestamp = timestamp.replace(second=0, minute=0)
                if timestamp not in free:
                    free[timestamp] = {"all":0, **{team:0 for team in TEAMS}} 
                    paid[timestamp] = {"all":0, **{team:0 for team in TEAMS}} 
                team = line.split("| TARIFF |")[1].split("charged")[0].strip()
                cost = int(line.split("charged")[1].split("HUF")[0])
                if cost > 0: 
                    paid[timestamp]["all"] += 1
                    paid[timestamp][team] += 1
                else: 
                    free[timestamp]["all"] += 1
                    free[timestamp][team] += 1
    for timestamp in free:
        df.loc[timestamp] = { 
            **{f"{team}-free": count for team,count in free[timestamp].items()},
            **{f"{team}-paid": count for team,count in paid[timestamp].items()}
        }
    df.sort_values(by="timestamp", inplace=True)
    for team in ["all", *TEAMS]:
        df[team] = df[f"{team}-free"] + df[f"{team}-paid"]

    df = df[df.index >= df.index[0] + pd.Timedelta(hours=ignore_hours)]

    df[TEAMS].plot(kind='area', stacked=True, figsize=SIZE)
    plt.title("Dockings at stations over time")
    plt.legend()
    plt.gca().set_xlabel("")
    plt.tight_layout()
    plt.savefig(f"{filename}_over_time.png")

    plt.clf() 

    df[[f"{team}-paid" for team in TEAMS]].plot(kind='area', stacked=True, figsize=SIZE)
    plt.title("Paid dockings at stations over time")
    plt.legend()
    plt.gca().set_xlabel("")
    plt.tight_layout()
    plt.savefig(f"{filename}_over_time_paid.png")

    plt.clf() 

    column_sums = df[TEAMS].sum()
    column_sums.plot(kind='pie', figsize=SIZE, autopct=lambda p: f'{p:.1f}%\n({int(p * column_sums.sum() / 100)})')
    
    plt.legend()
    plt.ylabel("")
    plt.title("Overall dockings")
    plt.tight_layout()
    plt.savefig(f"{filename}.png")

    df.to_excel(f"{filename}.xlsx", index=False)

        






