import { colorgenerator } from '../utils'

const Color = ({ id }) => {
  const color = colorgenerator.get(id)

  return (
    <div
      style={{
        borderRadius: '100%',
        width: 20,
        aspectRatio: 1,
        background: color,
        marginRight: 5,
        border: '3px solid white',
        outline: `1px solid ${color}`,
      }}
    />
  )
}

const Teams = ({ teams }) => {
  return (
    <div
      style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        background: 'rgba(0, 0, 0, 0.5)',
        color: '#4fc3f7',
        width: '100%',
        paddingTop: 10,
        paddingLeft: 10,
        paddingRight: 10,
        display: 'flex',
        justifyContent: 'space-evenly',
        flexWrap: 'wrap',
        backdropFilter: 'blur(5px)',
        borderTop: '1px solid rgba(255, 255, 255, 0.3)',
      }}
    >
      {teams.map((team) => (
        <div
          key={team.teams_id}
          style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            marginBottom: 10,
          }}
        >
          <Color id={team.teams_id} />
          {team.name}
        </div>
      ))}
    </div>
  )
}

export default Teams
