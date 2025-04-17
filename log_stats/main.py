from extractor import *
ADMIN_LOG_DIR = "admin_logs"
DOCKER_LOG_DIR = "docker_logs"
REPORT_DIR = "reports"
DOCKER_LOG_FILE = os.path.join(REPORT_DIR,"docker.log")
DOCKER_LOG_HOUR_IGNORE = 0

os.makedirs(REPORT_DIR, exist_ok=True)


admin_stats = [
    score_over_time,
    operational_drone_over_time,
]
docker_stats = [
    status_tariff,
    charging_tariff,
    docking_tariff,
]

admindata = get_admin_data(ADMIN_LOG_DIR)
for stat in admin_stats:
    stat(admindata, os.path.join(REPORT_DIR, stat.__name__))

prepare_docker_logs(DOCKER_LOG_DIR, DOCKER_LOG_FILE)
for stat in docker_stats:
    stat(DOCKER_LOG_FILE, os.path.join(REPORT_DIR, stat.__name__), ignore_hours = DOCKER_LOG_HOUR_IGNORE)
