function ActionPlanCard({ recommended_actions }) {

  if (!recommended_actions || !Array.isArray(recommended_actions)) {
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
          color: '#2563eb'
        }}
      >
        🚀 Recommended Actions
      </h2>

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '12px'
        }}
      >

        {
          recommended_actions.map((action, index) => (

            <div
              key={index}
              style={{
                backgroundColor: '#eff6ff',
                border: '1px solid #bfdbfe',
                padding: '15px',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'flex-start',
                gap: '12px'
              }}
            >

              <span
                style={{
                  backgroundColor: '#2563eb',
                  color: 'white',
                  width: '28px',
                  height: '28px',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '14px',
                  fontWeight: 'bold',
                  flexShrink: 0
                }}
              >
                {index + 1}
              </span>

              <p
                style={{
                  color: '#1e40af',
                  fontSize: '15px',
                  lineHeight: '1.5',
                  margin: 0
                }}
              >
                {action}
              </p>

            </div>
          ))
        }

        {
          recommended_actions.length === 0 && (
            <p style={{ color: '#999' }}>
              No actions recommended
            </p>
          )
        }

      </div>

    </div>
  )
}

export default ActionPlanCard
