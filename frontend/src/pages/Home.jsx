import { useState } from 'react'
import axios from 'axios'

import UploadForm from '../components/UploadForm'
import ATSCard from '../components/ATSCard'
import Skills from '../components/Skills'
import Suggestions from '../components/Suggestions'

function Home() {

  const [resume, setResume] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async () => {

    if (!resume || !jobDescription) {
      alert('Please upload resume and paste job description')
      return
    }

    try {

      setLoading(true)
      setError('')

      const formData = new FormData()

      formData.append('resume', resume)
      formData.append('job_description', jobDescription)

      const response = await axios.post(
        'https://ai-resume-analyser-kzwq.onrender.com/resume/analyze',
        formData
      )

      setResult(response.data)

    } catch (err) {

      console.log(err)

      setError('Failed to analyze resume')

    } finally {

      setLoading(false)
    }
  }

  return (

    <div
      style={{
        padding: '40px',
        maxWidth: '1000px',
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
        AI Resume Analyzer
      </h1>

      <div
        style={{
          backgroundColor: '#f5f5f5',
          padding: '25px',
          borderRadius: '10px',
          marginBottom: '30px'
        }}
      >

        <UploadForm
          setResume={setResume}
          setJobDescription={setJobDescription}
          handleSubmit={handleSubmit}
        />

      </div>

      {
        loading && (
          <h3 style={{ textAlign: 'center' }}>
            Analyzing Resume...
          </h3>
        )
      }

      {
        error && (
          <h3 style={{ color: 'red', textAlign: 'center' }}>
            {error}
          </h3>
        )
      }

      {
        result && (

          <div
            style={{
              backgroundColor: 'white',
              padding: '25px',
              borderRadius: '10px',
              boxShadow: '0px 0px 10px rgba(0,0,0,0.1)'
            }}
          >

            <ATSCard score={result.ats_score} />

            <div
              style={{
                display: 'flex',
                gap: '40px',
                marginTop: '20px',
                flexWrap: 'wrap'
              }}
            >

              <div>

                <Skills
                  title="Matched Skills"
                  items={result.matched_skills}
                />

              </div>

              <div>

                <Skills
                  title="Missing Skills"
                  items={result.missing_skills}
                />

              </div>

            </div>

            <div style={{ marginTop: '30px' }}>

              <h2>AI Analysis</h2>

              <div
                style={{
                  backgroundColor: '#f8f8f8',
                  padding: '20px',
                  borderRadius: '10px',
                  whiteSpace: 'pre-line',
                  lineHeight: '1.7'
                }}
              >
                {result.summary}
              </div>

            </div>

            <div style={{ marginTop: '30px' }}>

              <Suggestions
                suggestions={result.suggestions}
              />

            </div>

          </div>
        )
      }

    </div>
  )
}

export default Home
