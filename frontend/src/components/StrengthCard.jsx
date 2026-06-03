function StrengthCard({ strengths }) {

  if (!strengths || !Array.isArray(strengths)) {
    return null
  }

  return (

    <div
      style={{
        backgroundColor: '#f8fafc',
        padding: '25px',
        borderRadius: '12px',
        boxShadow: '0px 2px 10px rgba(0,0,0,0.1)',
        marginBottom: '25px'
      }}
    >

      <h2
        style={{
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          color: '#16a34a'
        }}
      >
        💪 Strengths
      </h2>

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '12px'
        }}
      >

        {
          strengths.map((strength, index) => (

            <div
              key={index}
              style={{
                backgroundColor: '#f0fdf4',
                border: '1px solid #bbf7d0',
                padding: '15px',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'flex-start',
                gap: '12px'
              }}
            >

              <span
                style={{
                  color: '#16a34a',
                  fontSize: '18px',
                  marginTop: '2px',
                  flexShrink: 0
                }}
              >
                ✓
              </span>

              <p
                style={{
                  color: '#166534',
                  fontSize: '15px',
                  lineHeight: '1.5',
                  margin: 0
                }}
              >
                {strength}
              </p>

            </div>
          ))
        }

        {
          strengths.length === 0 && (
            <p style={{ color: '#999' }}>
              No strengths identified
            </p>
          )
        }

      </div>

    </div>
  )
}

export default StrengthCard
