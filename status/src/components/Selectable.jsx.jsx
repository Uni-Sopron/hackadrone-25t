import { colorgenerator } from '../utils'

const Selectable = ({
  size = 64,
  id,
  pinned,
  onPin,
  onHover,
  colorId,
  overrideColor,
  padding,
  icon: Icon,
  ...rest
}) => {
  const color = colorgenerator.get(colorId)

  const handleMouseEnter = () => {
    if (onHover) {
      onHover(id)
    }
  }
  const handleMouseLeave = () => {
    if (onHover && !pinned) {
      onHover()
    }
  }

  const handleClick = () => {
    onPin(id)
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
        paddingTop: padding ? (size / 10) * 2 : 0,
      }}
    >
      <Icon
        size={size * 0.85}
        color={overrideColor ? overrideColor : color}
        {...rest}
      />
    </div>
  )
}
export default Selectable
