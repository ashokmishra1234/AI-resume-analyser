import { useState } from 'react'

import Home from './pages/Home'
import ResumeComparison from './pages/ResumeComparison'

function App() {

  const [currentPage, setCurrentPage] = useState('home')

  const navStyle = {
    padding: '20px',
    backgroundColor: '#2563eb',
    color: 'white',
    display: 'flex',
    gap: '20px',
    justifyContent: 'center',
    boxShadow: '0px 2px 10px rgba(0,0,0,0.1)'
  }

  const navButtonStyle = {
    padding: '10px 20px',
    backgroundColor: 'transparent',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: '600',
    borderRadius: '5px',
    transition: 'background-color 0.3s'
  }

  const activeButtonStyle = {
    ...navButtonStyle,
    backgroundColor: 'rgba(255, 255, 255, 0.3)'
  }

  return (

    <div>

      {/* Navigation */}
      <div style={navStyle}>

        <button
          onClick={() => setCurrentPage('home')}
          style={currentPage === 'home' ? activeButtonStyle : navButtonStyle}
          onMouseOver={(e) => e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.2)'}
          onMouseOut={(e) => {
            if (currentPage === 'home') {
              e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.3)'
            } else {
              e.target.style.backgroundColor = 'transparent'
            }
          }}
        >
          📋 Resume Analyzer
        </button>

        <button
          onClick={() => setCurrentPage('compare')}
          style={currentPage === 'compare' ? activeButtonStyle : navButtonStyle}
          onMouseOver={(e) => e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.2)'}
          onMouseOut={(e) => {
            if (currentPage === 'compare') {
              e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.3)'
            } else {
              e.target.style.backgroundColor = 'transparent'
            }
          }}
        >
          🔄 Compare Resumes
        </button>

      </div>

      {/* Page Content */}
      {currentPage === 'home' && <Home />}
      {currentPage === 'compare' && <ResumeComparison />}

    </div>
  )
}

export default App

