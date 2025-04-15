import { useEffect, useState } from 'react'
import { GeoJson, GeoJsonFeature, Map, Overlay } from 'pigeon-maps'
import Teams from './Teams'
import { colorgenerator } from '../utils'
import Details from './Details'
import Selectable from './Selectable.jsx'
import ChargingStationIcon from './ChargingStationIcon.jsx'
import PackageIcon from './PackageIcon'
import DroneIcon from './DroneIcon'
import MailBoxIcon from './MailBoxIcon.jsx'
import Stats from './Stats.jsx'

const DroneMap = ({ data }) => {
  const [ZOOM, setZoom] = useState(15)
  const [selectedId, setSelectedId] = useState(false)
  const [pinnedId, setPinnedId] = useState(null)
  const [selectedTeam, setSelectedTeam] = useState(null)
  const [showPackages, setShowPackages] = useState(true)

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        setPinnedId(null)
        setSelectedId(false)
        setSelectedTeam(null)
      }
    }

    window.addEventListener('keydown', handleKeyDown)

    return () => {
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [])

  const teams = data?.teams

  const search = (data, id) => {
    const result = data.find((d) => {
      if (selectedId) {
        return d[id] === selectedId
      } else if (pinnedId) {
        return d[id] === pinnedId
      }
    })
    return result
  }

  const details = (() => {
    const drone = search(data?.drones, 'drone_id')
    const pkg = search(data?.packages, 'package_id')

    return drone || pkg
  })()

  const lines = data?.drones
    .filter((drone) => drone.operational)
    .map((drone) => ({
      id: drone.drone_id,
      color: drone.team_id,
      team_id: drone.team_id,
      path: {
        type: 'Feature',
        geometry: {
          type: 'LineString',
          coordinates: [
            [drone.source.longitude, drone.position.latitude],
            [drone.position.longitude, drone.position.latitude],
            [drone.destination.longitude, drone.destination.latitude],
          ],
        },
      },
    }))

  const package_line = (() => {
    const pkg = search(data.packages, 'package_id')
    if (!pkg) return null

    return {
      id: pkg.package_id,
      path: {
        type: 'Feature',
        geometry: {
          type: 'LineString',
          coordinates: [
            [pkg.position.longitude, pkg.position.latitude],
            [pkg.destination.longitude, pkg.destination.latitude],
          ],
        },
      },
    }
  })()

  const dronePackagesCorrectLocation = (() => {
    if (!data?.drones || !data?.packages || data?.packages.length === 0)
      return null

    const drone = search(data.drones, 'drone_id')
    if (!drone || drone.drone_id !== pinnedId) return null

    return drone.packages.map((pkg) => ({
      id: pkg.package_id,
      path: {
        type: 'Feature',
        geometry: {
          type: 'LineString',
          coordinates: [
            [drone.position.longitude, drone.position.latitude],
            [pkg.destination.longitude, pkg.destination.latitude],
          ],
        },
      },
    }))
  })()

  const correctPackageDestination = (() => {
    if (!data.drones) {
      return null
    }

    const drone = search(data.drones, 'drone_id')
    if (!drone || drone.drone_id !== pinnedId) return null

    return drone.packages
  })()

  const getDroneSize = (zoom) => {
    const minZoom = 13
    const maxZoom = 18
    const minSize = 100
    const maxSize = 200

    const t = (zoom - minZoom) / (maxZoom - minZoom)
    const clampedT = Math.max(0, Math.min(1, t))

    return minSize + clampedT * (maxSize - minSize)
  }

  const getCharginStationSize = (zoom) => {
    const minZoom = 13
    const maxZoom = 18
    const minSize = 60
    const maxSize = 150

    const t = (zoom - minZoom) / (maxZoom - minZoom)
    const clampedT = Math.max(0, Math.min(1, t))

    return minSize + clampedT * (maxSize - minSize)
  }

  const getPackageDestinationSize = (zoom) => {
    const minZoom = 13
    const maxZoom = 18
    const minSize = 60
    const maxSize = 150

    const t = (zoom - minZoom) / (maxZoom - minZoom)
    const clampedT = Math.max(0, Math.min(1, t))

    return minSize + clampedT * (maxSize - minSize)
  }

  const getPackageSize = (zoom) => {
    const minZoom = 13
    const maxZoom = 18
    const minSize = 90
    const maxSize = 120

    const t = (zoom - minZoom) / (maxZoom - minZoom)
    const clampedT = Math.max(0, Math.min(1, t))

    return minSize + clampedT * (maxSize - minSize)
  }

  const handleDetailClose = () => {
    setSelectedId()
    setPinnedId()
  }

  const handleHover = (id) => {
    if (id) {
      setSelectedId(id)
    } else {
      setSelectedId()
    }
  }

  const handlePin = (id) => {
    if (id === pinnedId) {
      setPinnedId()
    } else {
      setPinnedId(id)
    }
  }

  const handleTeamSelect = (team) => {
    if (team === selectedTeam) {
      setSelectedTeam()
    } else {
      setSelectedTeam(team)
      setSelectedId()
      setPinnedId()
    }
  }

  const teamFilter = (item) => {
    if (!selectedTeam) {
      return true
    }

    if (item.team_id === selectedTeam) {
      return true
    }
  }

  const handlePackageSelect = () => {
    setShowPackages((old) => !old)
  }

  return (
    <>
      <Map
        defaultCenter={[47.680268, 16.575547]}
        zoom={ZOOM}
        onBoundsChanged={({ zoom }) => {
          setZoom(zoom)
        }}
        animate
        attribution={false}
        zoomSnap={false}
      >
        {package_line && (
          <GeoJson
            svgAttributes={{
              strokeWidth: 5,
              stroke: colorgenerator.get(package_line.id),
              strokeDasharray: '12, 6',
              strokeOpacity: 0.8,
              strokeLinecap: 'round',
              filter: 'drop-shadow(0px 0px 3px rgba(0,0,0,0.2))',
              pathLength: '1',
              className: pinnedId !== package_line.id ? 'drone-path' : '',
            }}
          >
            <GeoJsonFeature feature={package_line.path} />
          </GeoJson>
        )}
        {dronePackagesCorrectLocation &&
          dronePackagesCorrectLocation.map((line) => (
            <GeoJson
              key={line.id}
              svgAttributes={{
                strokeWidth: 5,
                stroke: '#22c55e',
                strokeDasharray: '12, 6',
                strokeOpacity: 0.8,
                strokeLinecap: 'round',
                filter: 'drop-shadow(0px 0px 3px rgba(0,0,0,0.2))',
                pathLength: '1',
                className: '',
                opacity: '0.7',
              }}
            >
              <GeoJsonFeature feature={line.path} />
            </GeoJson>
          ))}
        {correctPackageDestination &&
          correctPackageDestination.map((pkg) => (
            <Overlay
              key={pkg.package_id}
              anchor={[pkg.destination.latitude, pkg.destination.longitude]}
              offset={[
                getPackageDestinationSize(ZOOM) / 2,
                getPackageDestinationSize(ZOOM) / 2,
              ]}
            >
              <MailBoxIcon
                size={getPackageDestinationSize(ZOOM)}
                color="#1E88E5"
              />
            </Overlay>
          ))}
        {data?.chargingStations.map((station) => (
          <Overlay
            key={station.station_id}
            anchor={[station.position.latitude, station.position.longitude]}
            offset={[
              getCharginStationSize(ZOOM) / 2,
              getCharginStationSize(ZOOM) / 2,
            ]}
          >
            <ChargingStationIcon
              size={getCharginStationSize(ZOOM)}
              color="#1E88E5"
            />
          </Overlay>
        ))}
        {showPackages &&
          data?.packages.map((pkg) => (
            <Overlay
              key={pkg.package_id}
              anchor={[pkg.position.latitude, pkg.position.longitude]}
              offset={[getPackageSize(ZOOM) / 2, getPackageSize(ZOOM) / 2]}
            >
              <Selectable
                id={pkg.package_id}
                icon={PackageIcon}
                size={getPackageSize(ZOOM)}
                colorId={pkg.contractor || pkg.package_id}
                overrideColor={
                  pkg.contractor
                    ? colorgenerator.get(pkg.contractor)
                    : '#FFD54F'
                }
                onHover={handleHover}
                onPin={handlePin}
                pinned={pkg.package_id === pinnedId}
              />
            </Overlay>
          ))}
        {lines.filter(teamFilter).map((line) => (
          <GeoJson
            key={line.id}
            svgAttributes={{
              strokeWidth: 5,
              stroke: colorgenerator.get(line.color),
              strokeDasharray: '12, 6',
              strokeOpacity: 1,
              strokeLinecap: 'round',
              filter: 'drop-shadow(0px 0px 3px rgba(0,0,0,0.2))',
              pathLength: '1',
              className: pinnedId !== line.id ? 'drone-path' : '',
            }}
          >
            <GeoJsonFeature feature={line.path} />
          </GeoJson>
        ))}
        {data?.drones.filter(teamFilter).map((drone, index) => {
          const droneIdNum = parseInt(
            drone.drone_id.replace(/\D/g, '') || index
          )
          const offsetMultiplier = 0.0001

          const angle = (droneIdNum % 8) * (Math.PI / 4)
          const latOffset = Math.sin(angle) * offsetMultiplier
          const lngOffset = Math.cos(angle) * offsetMultiplier

          return (
            <Overlay
              key={drone.drone_id}
              anchor={[
                drone.position.latitude + latOffset,
                drone.position.longitude + lngOffset,
              ]}
              offset={[
                getDroneSize(ZOOM) / 2 + latOffset,
                getDroneSize(ZOOM) / 2 + lngOffset,
              ]}
            >
              <Selectable
                id={drone.drone_id}
                icon={DroneIcon}
                size={getDroneSize(ZOOM)}
                colorId={drone.team_id}
                onHover={handleHover}
                onPin={handlePin}
                pinned={drone.drone_id === pinnedId}
                hasBox={drone.packages.length > 0}
                padding
                isOperational={drone.operational}
                charging={drone.state === 'charging'}
                moving={drone.state === 'moving'}
              />
            </Overlay>
          )
        })}
      </Map>
      <Details details={details} onClose={handleDetailClose} />

      <div
        style={{
          position: 'absolute',
          bottom: 0,
          zIndex: 1000,
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          pointerEvents: 'none',
        }}
      >
        <Stats stats={data} drones={data?.drones.filter(teamFilter)} />
        <div style={{ pointerEvents: 'auto' }}>
          <Teams
            teams={teams}
            onTeamSelect={handleTeamSelect}
            selectedTeam={selectedTeam}
            showPackages={showPackages}
            onPackageSelect={handlePackageSelect}
          />
        </div>
      </div>
    </>
  )
}

export default DroneMap
