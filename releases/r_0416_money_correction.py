import sys
import requests

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Api-Key": "5d8733d2-cc9b-48b2-9011-46ce3b1585b1"
}

with open(sys.argv[1]) as f:
    lines = f.readlines()

lines = [line.strip() for line in lines if "recharging drone" in line]

total_charge : dict[str,int] = {
    "Hubertus" : 0, 
    "FoxDrone" : 0,
    "Karesz" : 0,
    "RoadRunnerExpress" : 0
}

# TODO need to remove late logs
for line in lines:
    team = line.split("COMPANY | TARIFF | ")[1].split("charged")[0].strip()
    money = int(line.split("charged")[1].split("HUF")[0])
    print(team, money)
    try:
        total_charge[team] += money
    except KeyError:
        print(line)


exit()

for company_name, amount in total_charge.items():
    requests.post(
        "https://hackadrone.gazd.info/admin/donate", 
        json= {
            "company_name": company_name, 
            "amount_huf": amount
        }, headers=headers    
    )