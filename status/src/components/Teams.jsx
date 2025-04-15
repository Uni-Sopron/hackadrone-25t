import { colorgenerator } from '../utils'
import PackageIcon from './PackageIcon'

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

const Teams = ({
  teams,
  onTeamSelect,
  selectedTeam,
  showPackages,
  onPackageSelect,
}) => {
  const sortedTeams = [...teams].sort((a, b) => b.score - a.score)

  return (
    <div
      style={{
        bottom: 0,
        left: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        color: '#fff',
        width: '100%',
        padding: 10,
        display: 'flex',
        justifyContent: 'space-evenly',
        flexWrap: 'wrap',
        backdropFilter: 'blur(8px)',
        borderTop: '1px solid rgba(255, 255, 255, 0.2)',
        boxShadow: '0 -4px 12px rgba(0, 0, 0, 0.2)',
      }}
    >
      {sortedTeams.map((team) => {
        const isSelected = selectedTeam === team.name

        return (
          <div
            key={team.teams_id}
            style={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              padding: 6,
              transition: 'all 0.2s ease',
              cursor: 'pointer',
              backgroundColor: isSelected
                ? 'rgba(79, 195, 247, 0.2)'
                : 'transparent',
              borderRadius: '8px',
              border: isSelected
                ? '1px solid rgba(79, 195, 247, 0.5)'
                : '1px solid transparent',
              transform: isSelected ? 'scale(1.05)' : 'scale(1)',
              boxShadow: isSelected
                ? '0 0 8px rgba(79, 195, 247, 0.5)'
                : 'none',
            }}
            onClick={() => {
              onTeamSelect(team.name)
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
              <span
                style={{
                  fontWeight: isSelected ? 700 : 500,
                  color: isSelected ? '#ffffff' : '#fff',
                }}
              >
                {team.name}:
              </span>
              <strong
                style={{
                  marginLeft: '4px',
                  fontSize: '18px',
                  marginTop: 0,
                  color: isSelected ? '#ffffff' : '#4fc3f7',
                }}
              >
                {team.score}
              </strong>
            </div>
          </div>
        )
      })}
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          aspectRatio: 1,
          width: 40,
          transition: 'all 0.2s ease',
          cursor: 'pointer',
          backgroundColor: showPackages
            ? 'rgba(255, 213, 79, 0.2)'
            : 'transparent',
          borderRadius: '8px',
          border: showPackages
            ? '1px solid rgba(255, 213, 79, 0.5)'
            : '1px solid transparent',
        }}
        onClick={onPackageSelect}
        title={showPackages ? 'Hide Packages' : 'Show Packages'}
      >
        <PackageIcon
          size={32}
          color={showPackages ? '#FFD54F' : 'rgba(255, 255, 255, 0.6)'}
        />
      </div>
    </div>
  )
}

export default Teams
