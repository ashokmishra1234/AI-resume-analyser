import { useState } from 'react'
import axios from 'axios'

import ComparisonCard from '../components/ComparisonCard'
import SectionScoreCard from '../components/SectionScoreCard'
import Skills from '../components/Skills'

function ResumeComparison() {

  const [resume1, setResume1] = useState(null)
  const [resume2, setResume2] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleCompare = async () => {

    if (!resume1 || !resume2 || !jobDescription) {
      alert('Please upload both resumes and paste job description')
      return
    }

    try {

      setLoading(true)
      setError('')

      const formData = new FormData()

      formData.append('resume1', resume1)
      formData.append('resume2', resume2)
      formData.append('job_description', jobDescription)

      const response = await axios.post(
        'http://localhost:8000/resume/compare',
        formData
      )

      setResult(response.data)

    } catch (err) {

      console.log(err)

      setError('Failed to compare resumes')

    } finally {

      setLoading(false)
    }
  }

  return (

    <div
      style={{
        padding: '40px',
        maxWidth: '1200px',
        margin: 'auto',
        fontFamily: 'Arial'
      }}
    >

      <h1
        style={{
          textAlign: 'center',
          marginBottom: '30px'
        }}
      >
        Resume Comparison Tool
      </h1>

      {/* Input Section */}
      <div
        style={{
          backgroundColor: '#f5f5f5',
          padding: '25px',
          borderRadius: '10px',
          marginBottom: '30px'
        }}
      >

        <h2
          style={{
            marginBottom: '20px'
          }}
        >
          Upload Resumes & Job Description
        </h2>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '20px',
            marginBottom: '20px'
          }}
        >

          {/* Resume 1 Upload */}
          <div
            style={{
              backgroundColor: 'white',
              padding: '20px',
              borderRadius: '10px',
              border: '2px dashed #2563eb'
            }}
          >

            <label
              style={{
                display: 'block',
                marginBottom: '10px',
                fontWeight: '600',
                color: '#333'
              }}
            >
              📄 Resume 1
            </label>

            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setResume1(e.target.files[0])}
              style={{
                width: '100%',
                padding: '10px',
                borderRadius: '5px',
                border: '1px solid #e5e7eb'
              }}
            />

            {
              resume1 && (
                <p
                  style={{
                    marginTop: '10px',
                    color: '#16a34a',
                    fontSize: '14px'
                  }}
                >
                  ✅ {resume1.name} selected
                </p>
              )
            }

          </div>

          {/* Resume 2 Upload */}
          <div
            style={{
              backgroundColor: 'white',
              padding: '20px',
              borderRadius: '10px',
              border: '2px dashed #2563eb'
            }}
          >

            <label
              style={{
                display: 'block',
                marginBottom: '10px',
                fontWeight: '600',
                color: '#333'
              }}
            >
              📄 Resume 2
            </label>

            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setResume2(e.target.files[0])}
              style={{
                width: '100%',
                padding: '10px',
                borderRadius: '5px',
                border: '1px solid #e5e7eb'
              }}
            />

            {
              resume2 && (
                <p
                  style={{
                    marginTop: '10px',
                    color: '#16a34a',
                    fontSize: '14px'
                  }}
                >
                  ✅ {resume2.name} selected
                </p>
              )
            }

          </div>

        </div>

        {/* Job Description */}
        <div
          style={{
            marginBottom: '20px'
          }}
        >

          <label
            style={{
              display: 'block',
              marginBottom: '10px',
              fontWeight: '600',
              color: '#333'
            }}
          >
            💼 Job Description
          </label>

          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description here..."
            style={{
              width: '100%',
              height: '150px',
              padding: '15px',
              borderRadius: '5px',
              border: '1px solid #e5e7eb',
              fontFamily: 'Arial',
              fontSize: '14px',
              boxSizing: 'border-box'
            }}
          />

        </div>

        {/* Compare Button */}
        <button
          onClick={handleCompare}
          style={{
            width: '100%',
            padding: '12px',
            backgroundColor: '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            fontSize: '16px',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'background-color 0.3s'
          }}
          onMouseOver={(e) => e.target.style.backgroundColor = '#1d4ed8'}
          onMouseOut={(e) => e.target.style.backgroundColor = '#2563eb'}
        >
          Compare Resumes
        </button>

      </div>

      {/* Loading State */}
      {
        loading && (
          <h3 style={{ textAlign: 'center', marginBottom: '30px' }}>
            Comparing Resumes...
          </h3>
        )
      }

      {/* Error State */}
      {
        error && (
          <h3 style={{ color: 'red', textAlign: 'center', marginBottom: '30px' }}>
            {error}
          </h3>
        )
      }

      {/* Results Section */}
      {
        result && (

          <div>

            {/* Comparison Overview */}
            <ComparisonCard
              resume1Score={result.comparison.resume1_score}
              resume2Score={result.comparison.resume2_score}
              winner={result.comparison.winner}
            />

            {/* Section Scores Comparison */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: '30px',
                marginBottom: '30px'
              }}
            >

              <div>
                <h3 style={{ marginBottom: '15px' }}>
                  Resume 1 - Section Scores
                </h3>
                <SectionScoreCard scores={result.resume1.section_scores} />
              </div>

              <div>
                <h3 style={{ marginBottom: '15px' }}>
                  Resume 2 - Section Scores
                </h3>
                <SectionScoreCard scores={result.resume2.section_scores} />
              </div>

            </div>

            {/* Skills Comparison */}
            <div
              style={{
                backgroundColor: 'white',
                padding: '25px',
                borderRadius: '10px',
                boxShadow: '0px 0px 10px rgba(0,0,0,0.1)'
              }}
            >

              <h2 style={{ marginBottom: '30px' }}>
                📊 Skills Comparison
              </h2>

              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: '1fr 1fr',
                  gap: '30px'
                }}
              >

                <div>
                  <Skills
                    title="Resume 1 - Matched"
                    items={result.resume1.matched_skills}
                  />

                  <div style={{ marginTop: '20px' }}>
                    <Skills
                      title="Resume 1 - Missing"
                      items={result.resume1.missing_skills}
                    />
                  </div>
                </div>

                <div>
                  <Skills
                    title="Resume 2 - Matched"
                    items={result.resume2.matched_skills}
                  />

                  <div style={{ marginTop: '20px' }}>
                    <Skills
                      title="Resume 2 - Missing"
                      items={result.resume2.missing_skills}
                    />
                  </div>
                </div>

              </div>

            </div>

          </div>
        )
      }

    </div>
  )
}

export default ResumeComparison
