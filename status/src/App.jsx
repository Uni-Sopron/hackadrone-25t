import useSWR from 'swr'
import { FullScreen, useFullScreenHandle } from 'react-full-screen'
import {
  ArrowPathIcon,
  ArrowsPointingOutIcon,
  PauseIcon,
  PlayIcon,
  XMarkIcon,
} from '@heroicons/react/24/solid'
import DroneMap from './components/DroneMap'
import { useEffect, useState } from 'react'
import Time from './components/Time'
import { isBefore } from 'date-fns'

const fetcher = (...args) => fetch(...args).then((res) => res.json())

const URL = `${import.meta.env.VITE_BACKEND_URL}/admin/status`
const REFRESH_INTERVAL = `${import.meta.env.VITE_REFRESH_INTERVAL}`
const REPLAY_URL = `${import.meta.env.VITE_REPLAY_URL}`

function App() {
  const handle = useFullScreenHandle()
  const [replay, setReplay] = useState(false)
  const [paused, setPaused] = useState(true)
  const [time, setTime] = useState(null)
  const [refreshSpeed, setRefreshSpeed] = useState(500)
  const { data, error, isLoading, mutate } = useSWR(URL, fetcher, {
    refreshInterval: replay ? 0 : REFRESH_INTERVAL,
  })

  useEffect(() => {
    const refetch = async () => {
      const res = await fetcher(REPLAY_URL)
      if (isBefore(new Date(res.time), new Date(data.time))) {
        setPaused(true)
        return
      }
      setTime(res.time)
      mutate(res, false)
    }

    let interval
    if (replay) {
      interval = setInterval(() => {
        if (!paused) {
          refetch()
        }
      }, refreshSpeed)
    }

    return () => {
      clearInterval(interval)
    }
  }, [replay, paused, refreshSpeed, mutate, data?.time])

  const handleReplay = () => {
    setReplay(true)
    setPaused((old) => !old)
  }

  const clearReplay = () => {
    setReplay(false)
    setPaused(true)
  }

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
      <button className="replay-button" onClick={handleReplay}>
        {replay ? (
          paused ? (
            <PlayIcon width={32} height={32} />
          ) : (
            <PauseIcon width={32} height={32} />
          )
        ) : (
          <ArrowPathIcon width={32} height={32} />
        )}
      </button>
      {replay && (
        <>
          <button className="clear-replay-button" onClick={clearReplay}>
            <XMarkIcon width={32} height={32} />
          </button>
          <div className="slider-container">
            <input
              type="range"
              min="10"
              max="500"
              value={refreshSpeed}
              onChange={(e) => setRefreshSpeed(Number(e.target.value))}
              className="speed-slider"
            />
            <span className="slider-value">{refreshSpeed}ms</span>
          </div>
        </>
      )}
      <FullScreen handle={handle}>
        {replay && time && <Time time={time} />}
        <DroneMap data={data} />
      </FullScreen>
    </div>
  )
}

export default App
