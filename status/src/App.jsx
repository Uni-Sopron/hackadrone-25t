import useSWR from 'swr'
import { FullScreen, useFullScreenHandle } from 'react-full-screen'
import { ArrowsPointingOutIcon } from '@heroicons/react/24/solid'
import DroneMap from './components/DroneMap'

const fetcher = (...args) => fetch(...args).then((res) => res.json())

const URL = `${import.meta.env.VITE_BACKEND_URL}/admin/status`
const REFRESH_INTERVAL = `${import.meta.env.VITE_REFRESH_INTERVAL}`

function App() {
  const handle = useFullScreenHandle()
  const { data, error, isLoading } = useSWR(URL, fetcher, {
    refreshInterval: REFRESH_INTERVAL,
  })

  if (isLoading) {
    return <div>Loading...</div>
  }

  if (error) {
    return <p>{error.message}</p>
  }

  return (
    <div className="fullscreen">
      <button className="fullscreen-button" onClick={handle.enter}>
        <ArrowsPointingOutIcon width={32} height={32} />
      </button>
      <FullScreen handle={handle}>
        <DroneMap data={data} />
      </FullScreen>
    </div>
  )
}

export default App
