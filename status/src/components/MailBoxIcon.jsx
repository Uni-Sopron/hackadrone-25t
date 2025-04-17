const MailBoxIcon = ({
  color = '#4A5568',
  flagColor = '#E53E3E',
  size = 64,
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 512 512"
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
  >
    {/* Post stand */}
    <rect x="220" y="400" width="40" height="90" rx="4" fill={color} />

    {/* Ground shadow */}
    <ellipse cx="240" cy="490" rx="60" ry="10" fill="#00000020" />

    {/* Mailbox base */}
    <rect x="100" y="200" width="280" height="200" rx="30" fill={color} />
    <rect
      x="100"
      y="200"
      width="280"
      height="200"
      rx="30"
      stroke="#00000030"
      strokeWidth="6"
    />

    {/* Mailbox opening */}
    <rect x="150" y="240" width="140" height="40" rx="8" fill="#FFFFFF" />
    <rect
      x="150"
      y="240"
      width="140"
      height="40"
      rx="8"
      stroke="#00000020"
      strokeWidth="2"
    />

    {/* Decorative details */}
    <rect x="130" y="310" width="220" height="4" rx="2" fill="#00000020" />
    <rect x="130" y="340" width="220" height="4" rx="2" fill="#00000020" />
    <rect x="130" y="370" width="220" height="4" rx="2" fill="#00000020" />

    {/* Door handle */}
    <circle cx="350" cy="300" r="10" fill="#333" />
    <circle cx="350" cy="300" r="5" fill="#555" />
  </svg>
)

export default MailBoxIcon
