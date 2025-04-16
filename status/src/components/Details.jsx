import { getPreciseDistance } from 'geolib'
import { XMarkIcon } from '@heroicons/react/24/solid'
import {
  formatDistanceToNow,
  isPast,
  formatDuration,
  intervalToDuration,
} from 'date-fns'
import { hu } from 'date-fns/locale'

const SPEED = 13
const CAPACITY = 100

const battery_color = (percentage) => {
  if (percentage < 20) {
    return '#ff5252'
  } else if (percentage < 50) {
    return '#ffab40'
  } else {
    return '#81c784'
  }
}

const calculateDistance = (source, destination) => {
  const distance = getPreciseDistance(source, destination, 0.1)
  return distance
}

const formatRemainingTime = (deadline) => {
  const deadlineDate = new Date(deadline)

  if (isPast(deadlineDate)) {
    return 'Lejárt'
  }

  return formatDistanceToNow(deadlineDate, {
    addSuffix: true,
    includeSeconds: true,
    locale: hu,
  })
}

const formatSeconds = (seconds) => {
  const duration = intervalToDuration({ start: 0, end: seconds * 1000 })

  return formatDuration(duration, {
    format: ['minutes', 'seconds'],
    locale: hu,
    delimiter: ' ',
  })
}

const Details = ({ details, onClose }) => {
  if (!details) {
    return null
  }

  const isDrone = details.drone_id
  const isPackage = details.package_id
  const weight =
    details?.weight?.toFixed(2) ||
    details?.packages.reduce((acc, c) => acc + c.weight, 0)
  const battery = (details?.battery * 100).toFixed(2)
  const state = details?.state
  const rewards = details?.packages?.reduce((acc, c) => acc + c.reward, 0)
  const distance = calculateDistance(details?.position, details?.destination)
  const remainingTime =
    ((details?.battery * CAPACITY) / details?.discharging_speed_w) * 3600

  return (
    <div
      style={{
        position: 'fixed',
        top: 10,
        left: 10,
        background: 'rgba(0, 0, 0, 0.5)',
        color: 'white',
        padding: 20,
        borderRadius: 5,
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)',
        zIndex: 1000,
        minWidth: 280,
        backdropFilter: 'blur(5px)',
      }}
    >
      <h3
        style={{
          marginTop: 0,
          color: '#4fc3f7',
          borderBottom: '1px solid rgba(255,255,255,0.2)',
          paddingBottom: 5,
          marginBottom: 10,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <span>{isDrone ? 'Drone Status' : 'Package Details'}</span>
        <button onClick={onClose} className="close-button">
          <XMarkIcon width={25} height={25} />
        </button>
      </h3>

      <div className="detail-line">
        <strong>{isDrone ? 'Drone ID' : 'Package ID'}:</strong>
        <span>{isDrone ? details.drone_id : details.package_id}</span>
      </div>

      {isDrone && (
        <>
          <div className="detail-line">
            <strong>Battery:</strong>
            <span>
              <div
                style={{
                  width: 100,
                  height: 18,
                  background: 'rgba(255, 255, 255, 0.2)',
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  position: 'relative',
                  boxShadow: 'inset 0 1px 3px rgba(0, 0, 0, 0.2)',
                }}
              >
                <span
                  style={{
                    zIndex: 10,
                    color: battery < 30 ? 'white' : 'black',
                    fontSize: 13,
                    marginTop: 2,
                    fontWeight: 'bold',
                    textShadow:
                      battery < 30 ? '0 0 2px rgba(0,0,0,0.5)' : 'none',
                  }}
                >
                  {battery}%
                </span>
                <div
                  style={{
                    width: `${battery}%`,
                    height: '100%',
                    backgroundColor: battery_color(battery),
                    position: 'absolute',
                    left: 0,
                    top: 0,
                    transition: 'width 0.5s ease-in-out',
                    backgroundImage:
                      'linear-gradient(to bottom, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 100%)',
                  }}
                />
              </div>
            </span>
          </div>

          {details.operational && (
            <div className="detail-line">
              <strong>TTD:</strong>
              <span>{formatSeconds(remainingTime)}</span>
            </div>
          )}

          <div className="detail-line">
            <strong>Status:</strong>
            <span>{state}</span>
          </div>

          {state === 'swapping' && (
            <div className="detail-line">
              <strong>Swap remaining time:</strong>
              <br />
              <span>
                {formatSeconds(details.swapping_time_remaining_s)}&nbsp; (
                {details.swapping_time_remaining_s}s)
              </span>
              <br />
            </div>
          )}

          <div className="detail-line">
            <strong>Team ID:</strong>
            <span>{details.team_id}</span>
          </div>

          <div className="detail-line">
            <strong>Package count:</strong>
            <span>{details.packages.length}</span>
          </div>

          {details.packages.length > 0 && (
            <>
              <div className="detail-line">
                <strong>Packages reward:</strong>
                <span>{rewards}</span>
              </div>
              <div className="detail-line">
                <strong>Packages weight:</strong>
                <span>{weight} kg</span>
              </div>
              <div className="detail-line">
                <strong>Package deadlines:</strong>
                {details.packages.map((pkg) => (
                  <>
                    <br />
                    <span>
                      {new Date(pkg.deadline).toLocaleTimeString('hu-HU')} (
                      {formatRemainingTime(pkg.deadline)})
                    </span>
                  </>
                ))}
                <br />
              </div>
            </>
          )}
        </>
      )}

      {isPackage && (
        <>
          <div className="detail-line">
            <strong>Package reward:</strong>
            <span>{details.reward} HUF</span>
          </div>

          <div className="detail-line">
            <strong>Package deadline:</strong>
            <span>
              {new Date(details.deadline).toLocaleTimeString('hu-HU')}
            </span>
          </div>
          <div className="detail-line">
            <strong>Expires:</strong>
            <span>{formatRemainingTime(details.deadline)}</span>
          </div>

          {details.contractor && (
            <div className="detail-line">
              <strong>Package contractor:</strong>
              <span>{details.contractor}</span>
            </div>
          )}
        </>
      )}

      <div className="detail-line">
        <strong>Position:</strong>
        <br />
        <span>
          {`${details.position.latitude.toFixed(8)},
            ${details.position.longitude.toFixed(8)}`}
        </span>
      </div>

      <div className="detail-line" style={{ marginBottom: 0 }}>
        <strong>Destination:</strong>
        <br />
        <span>
          {`${details.destination.latitude.toFixed(8)},
            ${details.destination.longitude.toFixed(8)}`}
        </span>
      </div>

      {distance > 0 && (
        <>
          <div className="detail-line">
            <strong>Distance to target:</strong>
            <span>{distance.toFixed(2)} m</span>
          </div>
          <div className="detail-line" style={{ marginBottom: 0 }}>
            <strong>ETA:</strong>
            <span>{formatSeconds(distance.toFixed(2) / SPEED)}</span>
          </div>
        </>
      )}
    </div>
  )
}

export default Details
