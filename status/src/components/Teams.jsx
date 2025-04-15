import { colorgenerator } from '../utils'

const Color = ({ id }) => {
  const color = colorgenerator.get(id)

  return (
    <div
      style={{
        borderRadius: '100%',
        width: 24,
        aspectRatio: 1,
        backgroundColor: color,
        marginRight: 8,
        border: '2px solid white',
      }}
    />
  )
}

const Teams = ({ teams }) => {
  const sortedTeams = [...teams].sort((a, b) => b.score - a.score)

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        color: '#fff',
        width: '100%',
        paddingTop: 10,
        paddingLeft: 10,
        paddingRight: 10,
        display: 'flex',
        justifyContent: 'space-evenly',
        flexWrap: 'wrap',
        backdropFilter: 'blur(8px)',
        borderTop: '1px solid rgba(255, 255, 255, 0.2)',
        boxShadow: '0 -4px 12px rgba(0, 0, 0, 0.2)',
      }}
    >
      {sortedTeams.map((team) => (
        <div
          key={team.teams_id}
          style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            marginBottom: 10,
            padding: 6,
            transition: 'all 0.2s ease',
          }}
        >
          <Color id={team.teams_id} />
          <div
            style={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              marginTop: 2,
            }}
          >
            <span style={{ fontWeight: 500 }}>{team.name}:</span>
            <strong
              style={{
                marginLeft: '4px',
                fontSize: '18px',
                marginTop: 0,
                color: '#4fc3f7',
              }}
            >
              {team.score}
            </strong>
          </div>
        </div>
      ))}
    </div>
  )
}

export default Teams
