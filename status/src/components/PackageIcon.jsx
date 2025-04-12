const PackageIcon = ({
  color = '#FFD54F',
  strokeColor = '#000',
  strokeWidth = 1,
  size = 64,
  ...rest
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 200 200"
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    style={{
      filter: 'drop-shadow(0 2px 3px rgba(0,0,0,0.2))',
    }}
    {...rest}
  >
    {/* Shadow under the box for depth */}
    <ellipse cx="100" cy="160" rx="60" ry="8" fill="rgba(0,0,0,0.2)" />

    <defs>
      <linearGradient id="packageGradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor={color} />
        <stop offset="100%" stopColor={`${color}99`} />
      </linearGradient>
    </defs>

    {/* Package body */}
    <rect
      x="40"
      y="50"
      width="120"
      height="110"
      rx="5"
      fill="url(#packageGradient)"
      stroke={strokeColor}
      strokeWidth={strokeWidth}
    />

    {/* Package details - tape */}
    <g>
      {/* Vertical tape */}
      <rect
        x="85"
        y="50"
        width="30"
        height="110"
        fill="#FFFFFF"
        opacity="0.8"
        stroke="#888888"
        strokeWidth="0.7"
      />

      {/* Horizontal tape */}
      <rect
        x="40"
        y="90"
        width="120"
        height="25"
        fill="#FFFFFF"
        opacity="0.8"
        stroke="#888888"
        strokeWidth="0.7"
      />

      {/* Center label */}
      <rect
        x="80"
        y="85"
        width="40"
        height="35"
        rx="2"
        fill="#F7F7F7"
        stroke="#DDDDDD"
        strokeWidth="0.5"
      />

      {/* Package label */}
      <rect
        x="60"
        y="130"
        width="80"
        height="15"
        rx="2"
        fill="#F7F7F7"
        stroke="#DDDDDD"
        strokeWidth="0.5"
      />

      {/* Label barcode lines */}
      <g stroke="#333333" strokeWidth="0.5" opacity="0.7">
        <line x1="65" y1="135" x2="65" y2="140" />
        <line x1="68" y1="135" x2="68" y2="140" />
        <line x1="70" y1="135" x2="70" y2="140" />
        <line x1="73" y1="135" x2="73" y2="140" />
        <line x1="78" y1="135" x2="78" y2="140" />
        <line x1="80" y1="135" x2="80" y2="140" />
        <line x1="83" y1="135" x2="83" y2="140" />
        <line x1="88" y1="135" x2="88" y2="140" />
        <line x1="90" y1="135" x2="90" y2="140" />
        <line x1="95" y1="135" x2="95" y2="140" />
        <line x1="99" y1="135" x2="99" y2="140" />
        <line x1="102" y1="135" x2="102" y2="140" />
        <line x1="104" y1="135" x2="104" y2="140" />
        <line x1="106" y1="135" x2="106" y2="140" />
        <line x1="110" y1="135" x2="110" y2="140" />
        <line x1="115" y1="135" x2="115" y2="140" />
        <line x1="120" y1="135" x2="120" y2="140" />
        <line x1="125" y1="135" x2="125" y2="140" />
        <line x1="130" y1="135" x2="130" y2="140" />
      </g>
    </g>
  </svg>
)

export default PackageIcon
