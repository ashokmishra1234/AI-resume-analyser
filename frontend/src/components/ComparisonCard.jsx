function ComparisonCard({ resume1Score, resume2Score, winner }) {

  const getVerdict = (score) => {

    if (score >= 80) {
      return "Excellent Match"
    }

    if (score >= 60) {
      return "Good Match"
    }

    if (score >= 40) {
      return "Average Match"
    }

    return "Needs Improvement"
  }

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

  const difference = Math.abs(resume1Score - resume2Score)

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
          marginBottom: '30px',
          textAlign: 'center'
        }}
      >
        🔄 Resume Comparison
      </h2>

      <div
        style={{
          display: 'flex',
          gap: '40px',
          marginBottom: '30px',
          flexWrap: 'wrap',
          justifyContent: 'space-around'
        }}
      >

        {/* Resume 1 */}
        <div
          style={{
            flex: '1',
            minWidth: '250px',
            padding: '20px',
            backgroundColor: 'white',
            borderRadius: '10px',
            boxShadow: '0px 1px 5px rgba(0,0,0,0.08)',
            border: winner === 'Resume 1' ? '2px solid #16a34a' : '1px solid #e5e7eb'
          }}
        >

          <h3
            style={{
              marginBottom: '15px',
              color: '#333'
            }}
          >
            📄 Resume 1
          </h3>

          <div
            style={{
              backgroundColor: '#e5e7eb',
              borderRadius: '20px',
              overflow: 'hidden',
              height: '35px',
              marginBottom: '15px'
            }}
          >

            <div
              style={{
                width: `${resume1Score}%`,
                backgroundColor: getColor(resume1Score),
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontWeight: 'bold',
                transition: '0.5s'
              }}
            >
              {resume1Score}%
            </div>

          </div>

          <h4
            style={{
              color: getColor(resume1Score),
              marginBottom: '5px'
            }}
          >
            {getVerdict(resume1Score)}
          </h4>

          <p
            style={{
              color: '#666',
              fontSize: '14px'
            }}
          >
            ATS Score: <strong>{resume1Score}</strong>
          </p>

        </div>

        {/* Resume 2 */}
        <div
          style={{
            flex: '1',
            minWidth: '250px',
            padding: '20px',
            backgroundColor: 'white',
            borderRadius: '10px',
            boxShadow: '0px 1px 5px rgba(0,0,0,0.08)',
            border: winner === 'Resume 2' ? '2px solid #16a34a' : '1px solid #e5e7eb'
          }}
        >

          <h3
            style={{
              marginBottom: '15px',
              color: '#333'
            }}
          >
            📄 Resume 2
          </h3>

          <div
            style={{
              backgroundColor: '#e5e7eb',
              borderRadius: '20px',
              overflow: 'hidden',
              height: '35px',
              marginBottom: '15px'
            }}
          >

            <div
              style={{
                width: `${resume2Score}%`,
                backgroundColor: getColor(resume2Score),
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontWeight: 'bold',
                transition: '0.5s'
              }}
            >
              {resume2Score}%
            </div>

          </div>

          <h4
            style={{
              color: getColor(resume2Score),
              marginBottom: '5px'
            }}
          >
            {getVerdict(resume2Score)}
          </h4>

          <p
            style={{
              color: '#666',
              fontSize: '14px'
            }}
          >
            ATS Score: <strong>{resume2Score}</strong>
          </p>

        </div>

      </div>

      {/* Winner Section */}
      <div
        style={{
          backgroundColor: '#f0fdf4',
          borderLeft: '4px solid #16a34a',
          padding: '20px',
          borderRadius: '8px',
          textAlign: 'center'
        }}
      >

        <h3
          style={{
            color: '#16a34a',
            marginBottom: '10px'
          }}
        >
          🏆 Winner
        </h3>

        {
          winner === 'Tie' ? (
            <p
              style={{
                fontSize: '18px',
                fontWeight: 'bold',
                color: '#16a34a'
              }}
            >
              Both resumes have equal scores!
            </p>
          ) : (
            <>
              <p
                style={{
                  fontSize: '18px',
                  fontWeight: 'bold',
                  color: '#16a34a',
                  marginBottom: '10px'
                }}
              >
                {winner}
              </p>

              <p
                style={{
                  color: '#666',
                  fontSize: '14px'
                }}
              >
                Difference: <strong>{difference} points</strong>
              </p>
            </>
          )
        }

      </div>

    </div>
  )
}

export default ComparisonCard
