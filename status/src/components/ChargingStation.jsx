export const ChargingStation = ({
  size = 32,
  color = '#4CAF50', // zöld default
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 256 256"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M160,44L160,212C160,214.208 158.208,216 156,216L52,216C49.792,216 48,214.208 48,212L48,44C48,41.792 49.792,40 52,40L156,40C158.208,40 160,41.792 160,44Z"
      style={{ fill: color }}
    />
    <path
      d="M112,72L80,136L104,136L96,184L128,120L104,120L112,72Z"
      style={{ fill: '#fff', fillRule: 'nonzero' }}
    />
    <path
      d="M160,72C176,72 192,88 192,104L192,152C192,168 176,184 160,184"
      style={{
        fill: 'none',
        fillRule: 'nonzero',
        stroke: color,
        strokeWidth: 4,
      }}
    />
    <path
      d="M184,96L184,112"
      style={{
        fill: 'none',
        fillRule: 'nonzero',
        stroke: color,
        strokeWidth: 4,
      }}
    />
    <path
      d="M200,96L200,112"
      style={{
        fill: 'none',
        fillRule: 'nonzero',
        stroke: color,
        strokeWidth: 4,
      }}
    />
  </svg>
)

export default ChargingStation
