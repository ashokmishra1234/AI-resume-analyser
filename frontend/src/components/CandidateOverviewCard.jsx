function CandidateOverviewCard({ overview, fit_level, interview_chance, resume_verdict }) {

  if (!overview || !fit_level || !interview_chance || !resume_verdict) {
    return null
  }

  const getVerdictIcon = () => {
    if (resume_verdict && resume_verdict.includes("Strong")) {
      return "🟢"
    } else if (resume_verdict && resume_verdict.includes("Good")) {
      return "🟡"
    } else if (resume_verdict.includes("Average")) {
      return "🟠"
    } else {
      return "🔴"
    }
  }

  const getVerdictColor = () => {
    if (resume_verdict && resume_verdict.includes("Strong")) {
      return "#16a34a"
    } else if (resume_verdict && resume_verdict.includes("Good")) {
      return "#f59e0b"
    } else if (resume_verdict.includes("Average")) {
      return "#f97316"
    } else {
      return "#dc2626"
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
          marginBottom: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}
      >
        👤 Candidate Overview
      </h2>

      <p
        style={{
          fontSize: '16px',
          lineHeight: '1.6',
          color: '#333',
          marginBottom: '25px'
        }}
      >
        {overview}
      </p>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '20px'
        }}
      >

        {/* Overall Fit */}
        <div
          style={{
            backgroundColor: 'white',
            padding: '15px',
            borderRadius: '10px',
            textAlign: 'center',
            border: '1px solid #e5e7eb'
          }}
        >

          <p
            style={{
              color: '#666',
              fontSize: '13px',
              marginBottom: '8px',
              fontWeight: '500'
            }}
          >
            Overall Fit
          </p>

          <p
            style={{
              fontSize: '28px',
              fontWeight: 'bold',
              color: '#2563eb'
            }}
          >
            {fit_level}
          </p>

        </div>

        {/* Interview Chance */}
        <div
          style={{
            backgroundColor: 'white',
            padding: '15px',
            borderRadius: '10px',
            textAlign: 'center',
            border: '1px solid #e5e7eb'
          }}
        >

          <p
            style={{
              color: '#666',
              fontSize: '13px',
              marginBottom: '8px',
              fontWeight: '500'
            }}
          >
            Interview Chance
          </p>

          <p
            style={{
              fontSize: '18px',
              fontWeight: 'bold',
              color: '#2563eb'
            }}
          >
            {interview_chance}
          </p>

        </div>

        {/* Resume Verdict */}
        <div
          style={{
            backgroundColor: 'white',
            padding: '15px',
            borderRadius: '10px',
            textAlign: 'center',
            border: '1px solid #e5e7eb'
          }}
        >

          <p
            style={{
              color: '#666',
              fontSize: '13px',
              marginBottom: '8px',
              fontWeight: '500'
            }}
          >
            Verdict
          </p>

          <p
            style={{
              fontSize: '18px',
              fontWeight: 'bold',
              color: getVerdictColor()
            }}
          >
            {getVerdictIcon()} {resume_verdict}
          </p>

        </div>

      </div>

    </div>
  )
}

export default CandidateOverviewCard
