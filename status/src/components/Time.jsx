import { format } from 'date-fns'
import { hu } from 'date-fns/locale'

const Time = ({ time }) => {
  return (
    <div className="time-container">
      <span style={{ marginTop: 3 }}>
        {format(new Date(time), 'PPpp', { locale: hu })}
      </span>
    </div>
  )
}

export default Time
