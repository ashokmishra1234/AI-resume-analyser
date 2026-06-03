function ImprovementCard({ improvement_areas }) {

  if (!improvement_areas || !Array.isArray(improvement_areas)) {
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
          color: '#f59e0b'
        }}
      >
        ⚠ Improvement Areas
      </h2>

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '12px'
        }}
      >

        {
          improvement_areas.map((area, index) => (

            <div
              key={index}
              style={{
                backgroundColor: '#fffbeb',
                border: '1px solid #fde68a',
                padding: '15px',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'flex-start',
                gap: '12px'
              }}
            >

              <span
                style={{
                  color: '#f59e0b',
                  fontSize: '18px',
                  marginTop: '2px',
                  flexShrink: 0
                }}
              >
                •
              </span>

              <p
                style={{
                  color: '#92400e',
                  fontSize: '15px',
                  lineHeight: '1.5',
                  margin: 0
                }}
              >
                {area}
              </p>

            </div>
          ))
        }

        {
          improvement_areas.length === 0 && (
            <p style={{ color: '#999' }}>
              No improvement areas identified
            </p>
          )
        }

      </div>

    </div>
  )
}

export default ImprovementCard
