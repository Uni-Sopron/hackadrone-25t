const battery_color = (percentage) => {
  if (percentage < 20) {
    return '#ff5252'
  } else if (percentage < 50) {
    return '#ffab40'
  } else {
    return '#81c784'
  }
}

const Details = ({ details }) => {
  if (!details) {
    return null
  }

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
        minWidth: 220,
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
        }}
      >
        Drone Status
      </h3>

      <div className="detail-line">
        <strong>Drone ID:</strong>
        <span>{details.drone_id}</span>
      </div>

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
                color: details.battery < 30 ? 'white' : 'black',
                fontSize: 13,
                marginTop: 2,
                fontWeight: 'bold',
                textShadow:
                  details.battery < 30 ? '0 0 2px rgba(0,0,0,0.5)' : 'none',
              }}
            >
              {details.battery}%
            </span>
            <div
              style={{
                width: `${details.battery}%`,
                height: '100%',
                background: battery_color(details.battery),
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

      <div className="detail-line">
        <strong>Status:</strong>
        <span>{details.status}</span>
      </div>

      <div className="detail-line">
        <strong>Team ID:</strong>
        <span>{details.team_id}</span>
      </div>

      <div className="detail-line">
        <strong>Package count:</strong>
        <span>{details.packages.length}</span>
      </div>

      <div className="detail-line" style={{ marginBottom: 0 }}>
        <strong>Package weight:</strong>
        <span>{details.current_payload} kg</span>
      </div>
    </div>
  )
}

export default Details
