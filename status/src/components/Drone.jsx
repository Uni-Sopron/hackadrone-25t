import { colorgenerator } from '../utils'
import DroneIcon from './DroneIcon'

const Drone = ({ size = 64, data, pinned, onPin, onHover, ...rest }) => {
  const color = colorgenerator.get(data.team_id)
  const hasPackages = data.packages.length > 0

  const handleMouseEnter = () => {
    if (onHover) {
      onHover(data.drone_id)
    }
  }
  const handleMouseLeave = () => {
    if (onHover && !pinned) {
      onHover()
    }
  }

  const handleClick = () => {
    onPin(data.drone_id)
  }

  return (
    <div
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={handleClick}
      style={{
        width: size,
        height: size,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        cursor: 'pointer',
        outline: pinned ? '3px solid rgba(255, 50, 50, 0.8)' : 'none',
        borderRadius: '50%',
        background: pinned ? 'rgba(255, 255, 255, 0.55)' : 'transparent',
        boxShadow: pinned ? '0 0 15px rgba(0, 0, 0, 0.75)' : 'none',
        transition: 'all 0.2s ease-out',
        transform: pinned ? 'scale(1.05)' : 'scale(1)',
        paddingTop: (size / 10) * 2,
      }}
    >
      <DroneIcon
        size={size * 0.85}
        color={color}
        hasBox={hasPackages}
        {...rest}
      />
    </div>
  )
}
export default Drone
