import React from 'react'

const ChargingStation = ({
  size = 32,
  color = '#4CAF50',
  strokeColor = '#333',
  strokeWidth = 1.5,
  ...rest
}) => {
  // Create unique gradient ID
  const gradientId = `chargerGradient-${Math.random()
    .toString(36)
    .substr(2, 9)}`

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 256 256"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{
        filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))',
      }}
      {...rest}
    >
      {/* Define gradients */}
      <defs>
        <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor={color} />
          <stop offset="100%" stopColor={`${color}99`} />
        </linearGradient>
      </defs>

      {/* Base shadow */}
      <ellipse cx="104" cy="228" rx="60" ry="8" fill="rgba(0,0,0,0.15)" />

      {/* Base platform */}
      <rect
        x="44"
        y="216"
        width="120"
        height="12"
        rx="4"
        fill="#555555"
        stroke={strokeColor}
        strokeWidth={strokeWidth}
      />

      {/* Main charger body with rounded corners */}
      <rect
        x="48"
        y="44"
        width="112"
        height="172"
        rx="12"
        fill={`url(#${gradientId})`}
        stroke={strokeColor}
        strokeWidth={strokeWidth}
      />

      {/* Lightning bolt icon */}
      <path
        d="M112,76L86,124L104,124L96,156L122,108L104,108L112,76Z"
        style={{
          fill: 'white',
          stroke: strokeColor,
          strokeWidth: strokeWidth / 2,
        }}
      />

      {/* Charging wire */}
      <path
        d="M160,96C176,92 192,104 192,120L192,152C192,168 176,184 160,184"
        style={{
          fill: 'none',
          stroke: '#555555',
          strokeWidth: 6,
          strokeLinecap: 'round',
        }}
      />

      {/* Charging connector */}
      <rect
        x="160"
        y="172"
        width="24"
        height="16"
        rx="4"
        fill="#777777"
        stroke={strokeColor}
        strokeWidth={strokeWidth / 2}
      />

      {/* Connector pins */}
      <path
        d="M172,172L172,162"
        style={{
          fill: 'none',
          stroke: '#999999',
          strokeWidth: 3,
          strokeLinecap: 'round',
        }}
      />

      {/* Status lights */}
      <circle cx="76" cy="204" r="6" fill="#4FC3F7" />
      <circle cx="96" cy="204" r="6" fill="#FFEB3B" />
      <circle cx="116" cy="204" r="6" fill="#FF9800" />

      {/* Available charging slots indicator */}
      <rect
        x="132"
        y="196"
        width="16"
        height="16"
        rx="2"
        fill="white"
        stroke={strokeColor}
        strokeWidth={strokeWidth / 2}
      />

      <text
        x="140"
        y="210"
        textAnchor="middle"
        style={{
          fill: '#333',
          fontSize: '14px',
          fontWeight: 'bold',
          fontFamily: 'sans-serif',
        }}
      >
        2
      </text>

      {/* Control buttons */}
      <circle
        cx="75"
        cy="180"
        r="5"
        fill="#eee"
        stroke="#ccc"
        strokeWidth="0.5"
      />
      <circle
        cx="95"
        cy="180"
        r="5"
        fill="#eee"
        stroke="#ccc"
        strokeWidth="0.5"
      />
    </svg>
  )
}

export default ChargingStation
