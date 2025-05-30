import ChargingStationIcon from './ChargingStationIcon'
import DroneIcon from './DroneIcon'
import PackageIcon from './PackageIcon'

const Stats = ({ stats, drones }) => {
  const packageCount = stats?.packages.length
  const stationCount = stats?.chargingStations.length

  const packageDroneCount = drones.filter(
    (drone) => drone.packages.length > 0 && drone.state === 'moving'
  ).length
  const emptyDroneCount = drones.filter(
    (drone) => drone.packages.length === 0 && drone.state === 'moving'
  ).length

  const idleWithPackageCount = drones.filter(
    (drone) => drone.state === 'idle' && drone.packages.length > 0
  ).length
  const idleEmptyCount = drones.filter(
    (drone) => drone.state === 'idle' && drone.packages.length === 0
  ).length

  const diedWithPackageDroneCount = drones.filter(
    (drone) => !drone.operational && drone.packages.length > 0
  ).length
  const diedEmptyDroneCount = drones.filter(
    (drone) => !drone.operational && drone.packages.length === 0
  ).length

  const chargingDronesCount = drones.filter(
    (drone) => drone.state === 'charging'
  ).length

  return (
    <div
      style={{
        background: 'rgba(0, 0, 0, 0.5)',
        color: 'white',
        padding: 10,
        borderRadius: 5,
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)',
        zIndex: 1000,
        minWidth: 50,
        backdropFilter: 'blur(5px)',
        alignSelf: 'flex-end',
        marginRight: 10,
        marginBottom: 10,
        width: 100,
      }}
    >
      <div className="stat-line">
        <DroneIcon size={30} hasBox isOperational moving color="white" />
        <span>{packageDroneCount}</span>
      </div>
      <div className="stat-line">
        <DroneIcon size={30} isOperational moving color="white" />
        <span>{emptyDroneCount}</span>
      </div>
      <div className="stat-line">
        <DroneIcon size={30} isOperational charging color="white" />
        <span>{chargingDronesCount}</span>
      </div>
      <div className="stat-line">
        <DroneIcon
          size={30}
          hasBox
          isOperational
          style={{ opacity: 0.5 }}
          color="white"
        />
        <span>{idleWithPackageCount}</span>
      </div>
      <div className="stat-line">
        <DroneIcon
          size={30}
          isOperational
          style={{ opacity: 0.5 }}
          color="white"
        />
        <span>{idleEmptyCount}</span>
      </div>
      <div className="stat-line">
        <DroneIcon size={30} isOperational={false} style={{ marginTop: -10 }} />
        <span>{diedEmptyDroneCount}</span>
      </div>
      <div className="stat-line">
        <DroneIcon
          size={30}
          isOperational={false}
          hasBox
          style={{ marginTop: -10 }}
        />
        <span>{diedWithPackageDroneCount}</span>
      </div>
      <div className="stat-line">
        <PackageIcon size={30} />
        <span>{packageCount}</span>
      </div>
      <div className="stat-line">
        <ChargingStationIcon size={30} color="#1E88E5" />
        <span>{stationCount}</span>
      </div>
    </div>
  )
}

export default Stats
