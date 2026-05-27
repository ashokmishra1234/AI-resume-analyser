function ATSCard({ score }) {

  const getVerdict = () => {

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

  const getColor = () => {

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
          marginBottom: '20px'
        }}
      >
        📊 ATS Score
      </h2>

      <div
        style={{
          backgroundColor: '#e5e7eb',
          borderRadius: '20px',
          overflow: 'hidden',
          height: '35px',
          width: '100%',
          marginBottom: '15px'
        }}
      >

        <div
          style={{
            width: `${score}%`,
            backgroundColor: getColor(),
            height: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontWeight: 'bold',
            transition: '0.5s'
          }}
        >
          {score}%
        </div>

      </div>

      <h3
        style={{
          color: getColor()
        }}
      >
        {getVerdict()}
      </h3>

    </div>
  )
}

export default ATSCard
