import { useState } from 'react'
import axios from 'axios'

import UploadForm from '../components/UploadForm'
import ATSCard from '../components/ATSCard'
import CandidateOverviewCard from '../components/CandidateOverviewCard'
import ResumeVerdictCard from '../components/ResumeVerdictCard'
import SectionFeedbackCard from '../components/SectionFeedbackCard'
import StrengthCard from '../components/StrengthCard'
import ImprovementCard from '../components/ImprovementCard'
import ActionPlanCard from '../components/ActionPlanCard'
import ResumeChecklist from '../components/ResumeChecklist'
import SectionScoreCard from '../components/SectionScoreCard'
import Skills from '../components/Skills'

function Home({ token }) {

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
        'http://localhost:8000/resume/analyze',
        formData,
        { headers: { Authorization: `Bearer ${token}` } }
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

            {/* Section 1: Verdict and Overview */}
            {
              result.resume_verdict && (
                <ResumeVerdictCard
                  resume_verdict={result.resume_verdict}
                  ats_score={result.ats_score}
                  interview_chance={result.interview_chance}
                  fit_level={result.fit_level}
                />
              )
            }

            {
              result.candidate_overview && (
                <CandidateOverviewCard
                  overview={result.candidate_overview}
                  fit_level={result.fit_level}
                  interview_chance={result.interview_chance}
                  resume_verdict={result.resume_verdict}
                />
              )
            }

            {/* Section 2: Analysis Cards */}
            {result.strengths && <StrengthCard strengths={result.strengths} />}

            {result.improvement_areas && <ImprovementCard improvement_areas={result.improvement_areas} />}

            {result.recommended_actions && <ActionPlanCard recommended_actions={result.recommended_actions} />}

            {/* Section 3: Detailed Breakdown */}
            {
              result.section_scores && result.section_feedback && (
                <SectionFeedbackCard
                  section_scores={result.section_scores}
                  section_feedback={result.section_feedback}
                />
              )
            }

            {result.section_scores && <SectionScoreCard scores={result.section_scores} />}

            {/* Section 4: Skills Analysis */}
            <div
              style={{
                backgroundColor: '#f8fafc',
                padding: '25px',
                borderRadius: '12px',
                boxShadow: '0px 2px 10px rgba(0,0,0,0.1)',
                marginBottom: '25px'
              }}
            >

              <h2 style={{ marginBottom: '20px' }}>
                🎯 Skills Analysis
              </h2>

              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: '1fr 1fr',
                  gap: '25px',
                  marginBottom: '25px'
                }}
              >

                <div>
                  {result.matched_skills && (
                    <Skills
                      title="Matched Skills"
                      items={result.matched_skills}
                    />
                  )}
                </div>

                <div>
                  {result.skill_priorities && result.skill_priorities.length > 0 ? (
                    <div
                      style={{
                        backgroundColor: '#f8fafc',
                        padding: '20px',
                        borderRadius: '12px',
                        boxShadow: '0px 2px 10px rgba(0,0,0,0.08)',
                        minWidth: '250px',
                        flex: '1'
                      }}
                    >

                      <h2
                        style={{
                          marginBottom: '15px',
                          color: '#dc2626'
                        }}
                      >
                        ❌ Missing Skills (By Priority)
                      </h2>

                      <ul
                        style={{
                          paddingLeft: '20px'
                        }}
                      >

                        {
                          result.skill_priorities.map((item, index) => (

                            <li
                              key={index}
                              style={{
                                marginBottom: '10px',
                                color: '#b91c1c',
                                fontWeight: '500',
                                textTransform: 'capitalize',
                                display: 'flex',
                                justifyContent: 'space-between'
                              }}
                            >

                              <span>{item.skill}</span>

                              <span
                                style={{
                                  fontSize: '12px',
                                  fontWeight: '600',
                                  padding: '2px 8px',
                                  borderRadius: '4px',
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

                            </li>
                          ))
                        }

                      </ul>

                    </div>
                  ) : (
                    <div>
                      {result.missing_skills && (
                        <Skills
                          title="Missing Skills"
                          items={result.missing_skills}
                        />
                      )}
                    </div>
                  )}
                </div>

              </div>

            </div>

            {/* Section 5: Resume Audit */}
            {result.resume_audit && <ResumeChecklist resume_audit={result.resume_audit} />}

          </div>
        )
      }

    </div>
  )
}

export default Home
