function ResumeChecklist({ resume_audit }) {

  if (!resume_audit || !resume_audit.found || !resume_audit.missing) {
    return null
  }

  const found_items = resume_audit.found || []
  const missing_items = resume_audit.missing || []
  const total_items = found_items.length + missing_items.length
  const completion_percentage = total_items > 0 ? Math.round((found_items.length / total_items) * 100) : 0

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
          marginBottom: '25px'
        }}
      >
        📋 Resume Audit
      </h2>

      {/* Completeness Score Section */}
      <div
        style={{
          backgroundColor: 'white',
          padding: '25px',
          borderRadius: '10px',
          marginBottom: '30px',
          textAlign: 'center',
          border: '1px solid #e5e7eb'
        }}
      >

        <p
          style={{
            color: '#666',
            fontSize: '14px',
            marginBottom: '12px',
            fontWeight: '600'
          }}
        >
          Resume Completeness Score
        </p>

        <h3
          style={{
            fontSize: '48px',
            fontWeight: 'bold',
            color: '#2563eb',
            margin: '0 0 20px 0'
          }}
        >
          {completion_percentage}%
        </h3>

        {/* Progress Bar */}
        <div
          style={{
            backgroundColor: '#e5e7eb',
            borderRadius: '8px',
            overflow: 'hidden',
            height: '12px',
            marginBottom: '15px'
          }}
        >

          <div
            style={{
              width: `${completion_percentage}%`,
              backgroundColor: '#2563eb',
              height: '100%',
              transition: 'width 0.5s ease'
            }}
          />

        </div>

        <p
          style={{
            color: '#666',
            fontSize: '14px',
            margin: 0
          }}
        >
          {found_items.length} / {total_items} Sections Present
        </p>

      </div>

      {/* Found In Resume Section */}
      {
        found_items.length > 0 && (

          <div
            style={{
              marginBottom: '30px'
            }}
          >

            <h3
              style={{
                color: '#16a34a',
                marginBottom: '15px',
                fontSize: '16px',
                fontWeight: '600'
              }}
            >
              ✓ Found In Resume ({found_items.length})
            </h3>

            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '10px'
              }}
            >

              {
                found_items.map((item, index) => (

                  <div
                    key={index}
                    style={{
                      backgroundColor: '#f0fdf4',
                      border: '1px solid #bbf7d0',
                      padding: '12px 15px',
                      borderRadius: '8px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between'
                    }}
                  >

                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px'
                      }}
                    >

                      <span
                        style={{
                          color: '#16a34a',
                          fontSize: '16px',
                          fontWeight: 'bold'
                        }}
                      >
                        ✓
                      </span>

                      <p
                        style={{
                          color: '#15803d',
                          fontSize: '14px',
                          margin: 0,
                          fontWeight: '500'
                        }}
                      >
                        {item.name}
                      </p>

                    </div>

                    {
                      item.priority && (

                        <span
                          style={{
                            fontSize: '11px',
                            fontWeight: '600',
                            padding: '3px 8px',
                            borderRadius: '10px',
                            backgroundColor:
                              item.priority === 'High' ? '#fecaca' :
                              item.priority === 'Medium' ? '#fed7aa' :
                              '#e5e7eb',
                            color:
                              item.priority === 'High' ? '#7f1d1d' :
                              item.priority === 'Medium' ? '#92400e' :
                              '#4b5563'
                          }}
                        >
                          {item.priority}
                        </span>
                      )
                    }

                  </div>
                ))
              }

            </div>

          </div>
        )
      }

      {/* Missing From Resume Section */}
      {
        missing_items.length > 0 && (

          <div>

            <h3
              style={{
                color: '#dc2626',
                marginBottom: '15px',
                fontSize: '16px',
                fontWeight: '600'
              }}
            >
              ✗ Missing From Resume ({missing_items.length})
            </h3>

            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '10px'
              }}
            >

              {
                missing_items.map((item, index) => (

                  <div
                    key={index}
                    style={{
                      backgroundColor: '#fef2f2',
                      border: '1px solid #fecaca',
                      padding: '12px 15px',
                      borderRadius: '8px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between'
                    }}
                  >

                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px'
                      }}
                    >

                      <span
                        style={{
                          color: '#dc2626',
                          fontSize: '16px',
                          fontWeight: 'bold'
                        }}
                      >
                        ✗
                      </span>

                      <p
                        style={{
                          color: '#b91c1c',
                          fontSize: '14px',
                          margin: 0,
                          fontWeight: '500'
                        }}
                      >
                        {item.name}
                      </p>

                    </div>

                    {
                      item.priority && (

                        <span
                          style={{
                            fontSize: '11px',
                            fontWeight: '600',
                            padding: '3px 8px',
                            borderRadius: '10px',
                            backgroundColor:
                              item.priority === 'High' ? '#fecaca' :
                              item.priority === 'Medium' ? '#fed7aa' :
                              '#e5e7eb',
                            color:
                              item.priority === 'High' ? '#7f1d1d' :
                              item.priority === 'Medium' ? '#92400e' :
                              '#4b5563'
                          }}
                        >
                          {item.priority}
                        </span>
                      )
                    }

                  </div>
                ))
              }

            </div>

          </div>
        )
      }

      {/* Empty State */}
      {
        found_items.length === 0 && missing_items.length === 0 && (

          <div
            style={{
              textAlign: 'center',
              padding: '40px',
              color: '#999'
            }}
          >

            <p>No audit data available</p>

          </div>
        )
      }

    </div>
  )
}

export default ResumeChecklist

