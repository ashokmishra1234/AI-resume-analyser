function SectionFeedbackCard({ section_scores, section_feedback }) {

  if (!section_scores || !section_feedback) {
    return null
  }

  const getColor = (score) => {
    if (score >= 80) {
      return "#16a34a"
    } else if (score >= 60) {
      return "#f59e0b"
    } else if (score >= 40) {
      return "#ef4444"
    } else {
      return "#dc2626"
    }
  }

  const getBackgroundColor = (score) => {
    if (score >= 80) {
      return "#f0fdf4"
    } else if (score >= 60) {
      return "#fffbeb"
    } else if (score >= 40) {
      return "#fef2f2"
    } else {
      return "#fef2f2"
    }
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
          marginBottom: '25px'
        }}
      >
        📊 Section Feedback
      </h2>

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '20px'
        }}
      >

        {
          section_scores && Object.entries(section_scores).map(([section, score]) => (

            <div
              key={section}
              style={{
                backgroundColor: getBackgroundColor(score),
                border: `1px solid ${getColor(score)}`,
                borderOpacity: 0.3,
                padding: '20px',
                borderRadius: '10px'
              }}
            >

              {/* Section Header */}
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: '12px'
                }}
              >

                <h3
                  style={{
                    margin: 0,
                    color: '#333',
                    fontSize: '16px',
                    fontWeight: '600'
                  }}
                >
                  {section}
                </h3>

                <span
                  style={{
                    fontSize: '18px',
                    fontWeight: 'bold',
                    color: getColor(score)
                  }}
                >
                  {score}%
                </span>

              </div>

              {/* Progress Bar */}
              <div
                style={{
                  backgroundColor: '#e5e7eb',
                  borderRadius: '8px',
                  overflow: 'hidden',
                  height: '20px',
                  marginBottom: '12px'
                }}
              >

                <div
                  style={{
                    width: `${score}%`,
                    backgroundColor: getColor(score),
                    height: '100%',
                    transition: 'width 0.5s ease'
                  }}
                />

              </div>

              {/* Feedback Text */}
              <p
                style={{
                  margin: 0,
                  color: '#555',
                  fontSize: '14px',
                  lineHeight: '1.5'
                }}
              >
                {section_feedback && section_feedback[section] ? section_feedback[section] : "No feedback available"}
              </p>

            </div>
          ))
        }

      </div>

    </div>
  )
}

export default SectionFeedbackCard
