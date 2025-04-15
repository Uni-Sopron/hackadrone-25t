const DroneIcon = ({
  color = '#000',
  boxColor = '#FFD54F',
  strokeColor = '#000',
  strokeWidth = 1,
  size = 64,
  hasBox = false,
  isOperational,
  moving,
  charging = false,
  style,
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 500 500"
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    style={{
      animation: moving ? 'hover 4s ease-in-out infinite' : '',
      filter: 'drop-shadow(0 2px 3px rgba(0,0,0,0.2))',
      transform: !isOperational ? 'rotateX(180deg)' : '',
      ...style,
    }}
  >
    {/* Spinning propellers - only visible when moving or charging */}
    {moving && (
      <>
        {/* Left propeller */}
        <ellipse
          cx="98"
          cy="122"
          rx="75"
          ry="10"
          fill="rgba(200,200,200,0.4)"
          style={{
            transformOrigin: '98px 122px',
            animation: 'rotate 0.5s linear infinite',
          }}
        />

        {/* Right propeller */}
        <ellipse
          cx="402"
          cy="122"
          rx="75"
          ry="10"
          fill="rgba(200,200,200,0.4)"
          style={{
            transformOrigin: '402px 122px',
            animation: 'rotate 0.5s linear infinite',
          }}
        />
      </>
    )}

    {/* Drone body with stroke */}
    <path
      d="M402.442,122.139C402.442,129.055 397.044,134.671 390.395,134.671C375.785,134.671 327.959,122.139 327.959,122.139C327.959,122.139 375.785,109.607 390.395,109.607C397.044,109.607 402.442,115.222 402.442,122.139ZM420.003,122.139C420.003,115.222 425.401,109.607 432.05,109.607C446.66,109.607 494.486,122.139 494.486,122.139C494.486,122.139 446.66,134.671 432.05,134.671C425.401,134.671 420.003,129.055 420.003,122.139ZM79.997,142.624L79.997,113.528C79.997,108.487 83.931,104.394 88.778,104.394C93.624,104.394 97.558,108.487 97.558,113.528L97.558,142.624C106.842,144.572 113.843,153.113 113.843,163.341L113.843,164.074L178.37,164.074C180.609,148.785 193.314,137.055 208.633,137.055L291.367,137.055C306.686,137.055 319.391,148.785 321.63,164.074L386.157,164.074L386.157,163.341C386.157,153.113 393.158,144.572 402.442,142.624L402.442,113.528C402.442,108.487 406.376,104.394 411.222,104.394C416.069,104.394 420.003,108.487 420.003,113.528L420.003,142.624C429.287,144.572 436.288,153.113 436.288,163.341L436.288,185.338C436.288,197.002 427.185,206.471 415.972,206.471L406.473,206.471C395.26,206.471 386.157,197.002 386.157,185.338L386.157,183.42L321.98,183.42L321.98,197.941C321.98,199.945 321.802,201.905 321.461,203.807C341.171,221.651 353.455,246.791 353.455,274.627L353.455,318.767C353.444,323.153 350.023,326.703 345.806,326.703L345.405,326.703C343.47,326.703 341.614,325.902 340.248,324.476C338.882,323.051 338.117,321.118 338.123,319.105L338.123,274.627C338.123,252.844 329.393,232.989 315.087,218.064C309.472,225.216 300.928,229.786 291.367,229.786L208.633,229.786C199.072,229.786 190.528,225.216 184.913,218.064C170.607,232.989 161.877,252.844 161.877,274.627L161.877,318.636C161.883,320.774 161.071,322.826 159.621,324.339C158.17,325.853 156.2,326.703 154.145,326.703L153.354,326.703C149.601,326.703 146.555,323.543 146.545,319.639L146.545,274.627C146.545,246.791 158.829,221.651 178.539,203.807C178.198,201.905 178.02,199.945 178.02,197.941L178.02,183.42L113.843,183.42L113.843,185.338C113.843,197.002 104.74,206.471 93.527,206.471L84.028,206.471C72.815,206.471 63.712,197.002 63.712,185.338L63.712,163.341C63.712,153.113 70.713,144.572 79.997,142.624ZM79.997,122.139C79.997,129.055 74.599,134.671 67.95,134.671C53.34,134.671 5.514,122.139 5.514,122.139C5.514,122.139 53.34,109.607 67.95,109.607C74.599,109.607 79.997,115.222 79.997,122.139ZM97.558,122.139C97.558,115.222 102.956,109.607 109.605,109.607C124.215,109.607 172.041,122.139 172.041,122.139C172.041,122.139 124.215,134.671 109.605,134.671C102.956,134.671 97.558,129.055 97.558,122.139Z"
      fill={color}
      stroke={strokeColor}
      strokeWidth={strokeWidth}
    />

    {/* Improved charging indicator - larger and more visible */}
    {charging && (
      <>
        {/* Large glowing background for better visibility */}
        <circle
          cx="250"
          cy="150"
          r="90"
          fill="rgba(79, 195, 247, 0.15)"
          style={{
            animation: 'pulse 2s ease-in-out infinite',
          }}
        />

        {/* Charging cable - thicker */}
        <path
          d="M250,130 L250,80"
          stroke="#4fc3f7"
          strokeWidth="15"
          strokeLinecap="round"
          style={{
            filter: 'drop-shadow(0 0 5px #4fc3f7)',
          }}
        />

        {/* Larger charging bolt */}
        <path
          d="M225,80 L275,80 L245,120 L285,120 L215,180 L235,125 L195,125 Z"
          fill="#ffeb3b"
          stroke="#f57f17"
          strokeWidth="2"
          style={{
            filter: 'drop-shadow(0 0 8px rgba(255, 235, 59, 0.9))',
            animation: 'pulse 1.5s ease-in-out infinite',
          }}
        />

        {/* Larger battery indicator */}
        <rect
          x="200"
          y="190"
          width="100"
          height="30"
          rx="8"
          ry="8"
          stroke="#333"
          strokeWidth="3"
          fill="rgba(0,0,0,0.2)"
        />
        <rect
          x="204"
          y="194"
          width="0"
          height="22"
          fill="#4fc3f7"
          style={{
            animation: 'charge 3s ease-in-out infinite',
            transformOrigin: 'left center',
            filter: 'drop-shadow(0 0 5px #4fc3f7)',
          }}
        />

        {/* Plus and minus indicators */}
        <circle cx="215" cy="205" r="6" fill="white" />
        <rect x="212" y="202" width="6" height="2" fill="black" />
        <rect x="214" y="200" width="2" height="6" fill="black" />

        <circle cx="285" cy="205" r="6" fill="white" />
        <rect x="282" y="202" width="6" height="2" fill="black" />
      </>
    )}

    {/* Optional package with stroke and gradient */}
    {hasBox && (
      <>
        {/* Shadow under the box for depth */}
        <ellipse cx="250" cy="398" rx="55" ry="7" fill="rgba(0,0,0,0.2)" />

        <defs>
          <linearGradient
            id="packageGradient"
            x1="0%"
            y1="0%"
            x2="100%"
            y2="100%"
          >
            <stop offset="0%" stopColor={boxColor} />
            <stop offset="100%" stopColor={`${boxColor}99`} />
          </linearGradient>
        </defs>

        <path
          d="M329.995,257.083L329.995,372.956C329.995,386.909 318.668,398.236 304.716,398.236L195.284,398.236C181.332,398.236 170.005,386.909 170.005,372.956L170.005,257.083C170.005,243.131 181.332,231.803 195.284,231.803L304.716,231.803C318.668,231.803 329.995,243.131 329.995,257.083Z"
          fill={`url(#packageGradient)`}
          stroke={strokeColor}
          strokeWidth={strokeWidth}
        />

        {/* Add package details - tape */}
        <g>
          {/* Vertical tape */}
          <rect
            x="230"
            y="231.803"
            width="40"
            height="166.433"
            fill={`${boxColor}ff`}
            stroke={`${boxColor}`}
            strokeWidth="0.7"
          />

          {/* Vertical tape - using contrasting color for better visibility */}
          <rect
            x="230"
            y="231.803"
            width="40"
            height="166.433"
            fill="#FFFFFF"
            opacity="0.8"
            stroke="#888888"
            strokeWidth="0.7"
          />
        </g>
      </>
    )}

    {/* Animation definitions */}
    <defs>
      <style>
        {`
          @keyframes hover {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
          }

          @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }

          @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
          }

          @keyframes charge {
            0% { width: 0; }
            80% { width: 92px; }
            100% { width: 92px; }
          }
        `}
      </style>
    </defs>
  </svg>
)

export default DroneIcon
