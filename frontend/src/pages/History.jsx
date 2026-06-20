import { useState, useEffect } from 'react'
import axios from 'axios'

function History({ token }) {

  const [analyses, setAnalyses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    axios.get('http://localhost:8000/history/', {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => {
        setAnalyses(res.data)
        setLoading(false)
      })
      .catch(() => {
        setError('Failed to load history')
        setLoading(false)
      })
  }, [])

  const getVerdictColor = (verdict) => {
    if (!verdict) return '#64748b'
    if (verdict.includes('Strong')) return '#16a34a'
    if (verdict.includes('Good')) return '#f59e0b'
    if (verdict.includes('Average')) return '#f97316'
    return '#dc2626'
  }

  const getScoreColor = (score) => {
    if (score >= 80) return '#16a34a'
    if (score >= 60) return '#f59e0b'
    if (score >= 40) return '#ef4444'
    return '#dc2626'
  }

  const formatDate = (isoString) => {
    const date = new Date(isoString)
    return date.toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div style={{
      padding: '40px',
      maxWidth: '900px',
      margin: 'auto',
      fontFamily: 'Arial'
    }}>

      <h1 style={{ textAlign: 'center', marginBottom: '10px' }}>
        Analysis History
      </h1>
      <p style={{ textAlign: 'center', color: '#64748b', marginBottom: '30px' }}>
        All your past resume analyses
      </p>

      {loading && (
        <h3 style={{ textAlign: 'center', color: '#64748b' }}>Loading history...</h3>
      )}

      {error && (
        <h3 style={{ textAlign: 'center', color: '#dc2626' }}>{error}</h3>
      )}

      {!loading && !error && analyses.length === 0 && (
        <div style={{
          textAlign: 'center',
          padding: '60px',
          backgroundColor: '#f8fafc',
          borderRadius: '12px',
          color: '#64748b'
        }}>
          <p style={{ fontSize: '18px', marginBottom: '10px' }}>No analyses yet</p>
          <p>Go to Resume Analyzer and upload your first resume!</p>
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {analyses.map((analysis) => (
          <div
            key={analysis.id}
            style={{
              backgroundColor: 'white',
              borderRadius: '12px',
              padding: '24px',
              boxShadow: '0px 2px 10px rgba(0,0,0,0.08)',
              border: '1px solid #e5e7eb'
            }}
          >

            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'flex-start',
              marginBottom: '16px',
              flexWrap: 'wrap',
              gap: '10px'
            }}>

              <span style={{ color: '#64748b', fontSize: '13px' }}>
                {formatDate(analysis.created_at)}
              </span>

              <span style={{
                backgroundColor: getVerdictColor(analysis.resume_verdict) + '20',
                color: getVerdictColor(analysis.resume_verdict),
                padding: '4px 12px',
                borderRadius: '20px',
                fontSize: '13px',
                fontWeight: '600'
              }}>
                {analysis.resume_verdict}
              </span>

            </div>

            <p style={{
              color: '#374151',
              fontSize: '14px',
              marginBottom: '16px',
              lineHeight: '1.5',
              backgroundColor: '#f8fafc',
              padding: '12px',
              borderRadius: '8px'
            }}>
              <strong>Job: </strong>{analysis.job_description_preview}
            </p>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '12px'
            }}>

              <div style={{
                textAlign: 'center',
                padding: '12px',
                backgroundColor: '#f8fafc',
                borderRadius: '8px'
              }}>
                <p style={{ color: '#64748b', fontSize: '12px', marginBottom: '4px' }}>ATS Score</p>
                <p style={{ fontSize: '24px', fontWeight: 'bold', color: getScoreColor(analysis.ats_score) }}>
                  {analysis.ats_score}%
                </p>
              </div>

              <div style={{
                textAlign: 'center',
                padding: '12px',
                backgroundColor: '#f8fafc',
                borderRadius: '8px'
              }}>
                <p style={{ color: '#64748b', fontSize: '12px', marginBottom: '4px' }}>Fit Level</p>
                <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#2563eb' }}>
                  {analysis.fit_level}
                </p>
              </div>

              <div style={{
                textAlign: 'center',
                padding: '12px',
                backgroundColor: '#f8fafc',
                borderRadius: '8px'
              }}>
                <p style={{ color: '#64748b', fontSize: '12px', marginBottom: '4px' }}>Interview Chance</p>
                <p style={{ fontSize: '16px', fontWeight: 'bold', color: getVerdictColor(analysis.resume_verdict) }}>
                  {analysis.interview_chance}
                </p>
              </div>

            </div>

          </div>
        ))}
      </div>

    </div>
  )
}

export default History
