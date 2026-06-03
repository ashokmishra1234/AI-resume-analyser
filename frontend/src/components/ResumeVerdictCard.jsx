function ResumeVerdictCard({ resume_verdict, ats_score, interview_chance, fit_level }) {

  if (!resume_verdict || ats_score === undefined || !interview_chance || !fit_level) {
    return null
  }

  const getVerdictIcon = () => {
    if (resume_verdict && resume_verdict.includes("Strong")) {
      return "🟢"
    } else if (resume_verdict.includes("Good")) {
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
    } else if (resume_verdict && resume_verdict.includes("Average")) {
      return "#f97316"
    } else {
      return "#dc2626"
    }
  }

  const getBackgroundColor = () => {
    if (resume_verdict && resume_verdict.includes("Strong")) {
      return "#f0fdf4"
    } else if (resume_verdict && resume_verdict.includes("Good")) {
      return "#fffbeb"
    } else if (resume_verdict && resume_verdict.includes("Average")) {
      return "#fff7ed"
    } else {
      return "#fef2f2"
    }
  }

  const getBorderColor = () => {
    if (resume_verdict && resume_verdict.includes("Strong")) {
      return "#bbf7d0"
    } else if (resume_verdict && resume_verdict.includes("Good")) {
      return "#fde68a"
    } else if (resume_verdict && resume_verdict.includes("Average")) {
      return "#fed7aa"
    } else {
      return "#fecaca"
    }
  }

  return (

    <div
      style={{
        backgroundColor: getBackgroundColor(),
        border: `2px solid ${getBorderColor()}`,
        padding: '30px',
        borderRadius: '12px',
        marginBottom: '25px',
        textAlign: 'center'
      }}
    >

      <h2
        style={{
          marginBottom: '20px',
          fontSize: '28px',
          color: getVerdictColor()
        }}
      >
        {getVerdictIcon()} Resume Verdict
      </h2>

      <h3
        style={{
          fontSize: '32px',
          fontWeight: 'bold',
          color: getVerdictColor(),
          marginBottom: '30px'
        }}
      >
        {resume_verdict}
      </h3>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '20px'
        }}
      >

        {/* ATS Score */}
        <div
          style={{
            backgroundColor: 'white',
            padding: '20px',
            borderRadius: '10px'
          }}
        >

          <p
            style={{
              color: '#666',
              fontSize: '13px',
              marginBottom: '10px',
              fontWeight: '500'
            }}
          >
            ATS Score
          </p>

          <p
            style={{
              fontSize: '32px',
              fontWeight: 'bold',
              color: getVerdictColor()
            }}
          >
            {ats_score}%
          </p>

        </div>

        {/* Interview Chance */}
        <div
          style={{
            backgroundColor: 'white',
            padding: '20px',
            borderRadius: '10px'
          }}
        >

          <p
            style={{
              color: '#666',
              fontSize: '13px',
              marginBottom: '10px',
              fontWeight: '500'
            }}
          >
            Interview Chance
          </p>

          <p
            style={{
              fontSize: '24px',
              fontWeight: 'bold',
              color: getVerdictColor()
            }}
          >
            {interview_chance}
          </p>

        </div>

        {/* Overall Fit */}
        <div
          style={{
            backgroundColor: 'white',
            padding: '20px',
            borderRadius: '10px'
          }}
        >

          <p
            style={{
              color: '#666',
              fontSize: '13px',
              marginBottom: '10px',
              fontWeight: '500'
            }}
          >
            Overall Fit
          </p>

          <p
            style={{
              fontSize: '32px',
              fontWeight: 'bold',
              color: getVerdictColor()
            }}
          >
            {fit_level}
          </p>

        </div>

      </div>

    </div>
  )
}

export default ResumeVerdictCard
