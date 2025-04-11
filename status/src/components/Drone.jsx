import { useState } from 'react'
import DroneIcon from './DroneIcon'

const Drone = ({ size = 64, data, onHover, ...rest }) => {
  const [hovered, setHovered] = useState(false)
  const handleMouseEnter = () => {
    setHovered(true)
    if (onHover) {
      onHover(data)
    }
  }
  const handleMouseLeave = () => {
    setHovered(false)
    if (onHover) {
      onHover(false)
    }
  }
  return (
    <div
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      style={{
        width: size,
        height: size,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <DroneIcon size={size} {...rest} />
    </div>
  )
}
export default Drone
