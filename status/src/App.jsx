import useSWR from 'swr'
import { GeoJson, GeoJsonFeature, Map, Marker, Overlay } from 'pigeon-maps'
import { useState } from 'react'
import Drone from './components/Drone'

const fetcher = (...args) => fetch(...args).then((res) => res.json())

const URL = `${import.meta.env.VITE_BACKEND_URL}/`

function App() {
  const [ZOOM, setZoom] = useState(15)
  const [details, setDetails] = useState(false)
  const { data, error, isLoading } = useSWR(URL, fetcher, {
    refreshInterval: 200,
  })

  if (isLoading) {
    return <div>Loading...</div>
  }

  if (error) {
    return <p>{error.message}</p>
  }

  const getDroneSize = (zoom) => {
    // Linear interpolation between min and max size
    const minZoom = 13
    const maxZoom = 18
    const minSize = 24
    const maxSize = 96

    const t = (zoom - minZoom) / (maxZoom - minZoom)
    const clampedT = Math.max(0, Math.min(1, t))

    return minSize + clampedT * (maxSize - minSize)
  }

  const handleHover = (drone) => {
    if (drone) {
      setDetails(drone)
      console.log('hovered', drone)
    } else {
      setDetails(false)
      console.log('unhovered')
    }
  }

  return (
    <div className="fullscreen">
      <Map
        defaultCenter={[47.680268, 16.575547]}
        defaultZoom={ZOOM}
        onBoundsChanged={({ center, zoom }) => {
          console.log('center', center)
          console.log('zoom', zoom)
          setZoom(zoom)
        }}
      >
        {data.map((drone) => (
          <GeoJson
            svgAttributes={{
              strokeWidth: '10',
              stroke: 'red',
              r: '20',
              pathLength: '1',
              className: 'drone-path',
            }}
            key={drone.drone_id}
          >
            <GeoJsonFeature feature={drone.path} />
          </GeoJson>
        ))}
        {data.map((drone) => (
          <Overlay
            key={drone.drone_id}
            anchor={[drone.position.latitude, drone.position.longitude]}
            offset={[getDroneSize(ZOOM) / 2, getDroneSize(ZOOM) / 2]}
          >
            <Drone
              size={getDroneSize(ZOOM)}
              data={drone}
              onHover={handleHover}
            />
          </Overlay>
        ))}
      </Map>
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          background: 'chucknorris',
          height: 200,
          width: 200,
        }}
      >
        {details && (
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              background: 'white',
              padding: 10,
            }}
          >
            <h3>Drone ID: {details.drone_id}</h3>
            <p>Altitude: {details.altitude}</p>
            <p>Speed: {details.speed}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
