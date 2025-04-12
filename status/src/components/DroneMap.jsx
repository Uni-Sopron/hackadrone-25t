import { useState } from 'react'
import { GeoJson, GeoJsonFeature, Map, Overlay } from 'pigeon-maps'
import Drone from './Drone'
import Teams from './Teams'
import { colorgenerator } from '../utils'
import Details from './Details'
import ChargingStation from './ChargingStation'
import PackageIcon from './PackageIcon'

const DroneMap = ({ data }) => {
  const [ZOOM, setZoom] = useState(15)
  const [selectedDrone, setSelectedDrone] = useState(false)
  const [pinnedDrone, setPinnedDrone] = useState(null)

  const teams = data?.teams

  const details = data?.drones.find((drone) => {
    if (selectedDrone) {
      return drone.drone_id === selectedDrone
    } else if (pinnedDrone) {
      return drone.drone_id === pinnedDrone
    }
  })

  const lines = data?.drones.map((drone) => ({
    id: drone.drone_id,
    path: {
      type: 'Feature',
      geometry: {
        type: 'LineString',
        coordinates: [
          [drone.source.longitude, drone.source.latitude],
          [drone.position.longitude, drone.position.latitude],
          [drone.destination.longitude, drone.destination.latitude],
        ],
      },
    },
  }))

  const getDroneSize = (zoom) => {
    const minZoom = 13
    const maxZoom = 18
    const minSize = 24
    const maxSize = 96

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

  const getPackageSize = (zoom) => {
    const minZoom = 13
    const maxZoom = 18
    const minSize = 40
    const maxSize = 120

    const t = (zoom - minZoom) / (maxZoom - minZoom)
    const clampedT = Math.max(0, Math.min(1, t))

    return minSize + clampedT * (maxSize - minSize)
  }

  const handleHover = (id) => {
    if (id) {
      setSelectedDrone(id)
    } else {
      setSelectedDrone()
    }
  }

  const handlePin = (id) => {
    if (id === pinnedDrone) {
      setPinnedDrone()
    } else {
      setPinnedDrone(id)
    }
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
        {lines.map((line) => (
          <GeoJson
            key={line.id}
            svgAttributes={{
              strokeWidth: 5,
              stroke: colorgenerator.get(line.id),
              strokeDasharray: '12, 6',
              strokeOpacity: 0.8,
              strokeLinecap: 'round',
              filter: 'drop-shadow(0px 0px 3px rgba(0,0,0,0.2))',
              pathLength: '1',
              className: pinnedDrone !== line.id && 'drone-path',
            }}
          >
            <GeoJsonFeature feature={line.path} />
          </GeoJson>
        ))}
        {data?.drones.map((drone) => (
          <Overlay
            key={drone.drone_id}
            anchor={[drone.position.latitude, drone.position.longitude]}
            offset={[getDroneSize(ZOOM) / 2, getDroneSize(ZOOM) / 2]}
          >
            <Drone
              size={getDroneSize(ZOOM)}
              data={drone}
              onHover={handleHover}
              onPin={handlePin}
              pinned={drone.drone_id === pinnedDrone}
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
            <ChargingStation
              size={getCharginStationSize(ZOOM)}
              color="#1E88E5"
            />
          </Overlay>
        ))}
        {data?.packages.map((pkg) => (
          <Overlay
            key={pkg.package_id}
            anchor={[pkg.position.latitude, pkg.position.longitude]}
            offset={[getPackageSize(ZOOM) / 2, getPackageSize(ZOOM) / 2]}
          >
            <PackageIcon size={getPackageSize(ZOOM)} />
          </Overlay>
        ))}
      </Map>
      <Details details={details} />
      <Teams teams={teams} />
    </>
  )
}

export default DroneMap
