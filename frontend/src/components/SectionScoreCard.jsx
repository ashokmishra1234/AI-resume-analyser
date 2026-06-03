function SectionScoreCard({ scores }) {

  const getColor = (score) => {

    if (score >= 80) {
      return "#16a34a"
    }

    if (score >= 60) {
      return "#f59e0b"
    }

    if (score >= 40) {
      return "#ef4444"
    }

    return "#dc2626"
  }

  return (

    <div
      style={{
        backgroundColor: '#f8fafc',
        padding: '25px',
        borderRadius: '12px',
        boxShadow: '0px 2px 10px rgba(0,0,0,0.1)',
        marginBottom: '30px'
      }}
    >

      <h2
        style={{
          marginBottom: '25px'
        }}
      >
        📈 Section Scores
      </h2>

      {
        Object.entries(scores).map(([section, score]) => (

          <div
            key={section}
            style={{
              marginBottom: '20px'
            }}
          >

            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                marginBottom: '8px'
              }}
            >

              <label
                style={{
                  fontWeight: '600',
                  color: '#333'
                }}
              >
                {section}
              </label>

              <span
                style={{
                  fontWeight: 'bold',
                  color: getColor(score)
                }}
              >
                {score}%
              </span>

            </div>

            <div
              style={{
                backgroundColor: '#e5e7eb',
                borderRadius: '10px',
                overflow: 'hidden',
                height: '25px',
                width: '100%'
              }}
            >

              <div
                style={{
                  width: `${score}%`,
                  backgroundColor: getColor(score),
                  height: '100%',
                  transition: 'width 0.5s ease',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'flex-end',
                  paddingRight: '8px',
                  color: 'white',
                  fontSize: '12px',
                  fontWeight: 'bold'
                }}
              >
                {score > 10 && `${score}%`}
              </div>

            </div>

          </div>

        ))
      }

    </div>
  )
}

export default SectionScoreCard
