import { useState, useEffect } from 'react'

import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'
import ResumeComparison from './pages/ResumeComparison'
import History from './pages/History'

function App() {

  const [user, setUser] = useState(null)
  const [currentPage, setCurrentPage] = useState('login')

  // On first load, check if user is already logged in (token in localStorage)
  useEffect(() => {
    const token = localStorage.getItem('token')
    const username = localStorage.getItem('username')
    if (token && username) {
      setUser({ token, username })
      setCurrentPage('home')
    }
  }, [])

  const handleLogin = (token, username) => {
    localStorage.setItem('token', token)
    localStorage.setItem('username', username)
    setUser({ token, username })
    setCurrentPage('home')
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    setUser(null)
    setCurrentPage('login')
  }

  // Show login/register pages if not logged in
  if (!user) {
    if (currentPage === 'register') {
      return <Register onLogin={handleLogin} goToLogin={() => setCurrentPage('login')} />
    }
    return <Login onLogin={handleLogin} goToRegister={() => setCurrentPage('register')} />
  }

  const navStyle = {
    padding: '16px 30px',
    backgroundColor: '#2563eb',
    color: 'white',
    display: 'flex',
    gap: '12px',
    alignItems: 'center',
    boxShadow: '0px 2px 10px rgba(0,0,0,0.1)'
  }

  const navButtonStyle = {
    padding: '8px 18px',
    backgroundColor: 'transparent',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
    fontSize: '15px',
    fontWeight: '600',
    borderRadius: '6px',
    transition: 'background-color 0.2s'
  }

  const activeButtonStyle = {
    ...navButtonStyle,
    backgroundColor: 'rgba(255, 255, 255, 0.25)'
  }

  return (
    <div>

      {/* Navigation */}
      <div style={navStyle}>

        <button
          onClick={() => setCurrentPage('home')}
          style={currentPage === 'home' ? activeButtonStyle : navButtonStyle}
        >
          Resume Analyzer
        </button>

        <button
          onClick={() => setCurrentPage('compare')}
          style={currentPage === 'compare' ? activeButtonStyle : navButtonStyle}
        >
          Compare Resumes
        </button>

        <button
          onClick={() => setCurrentPage('history')}
          style={currentPage === 'history' ? activeButtonStyle : navButtonStyle}
        >
          History
        </button>

        {/* Push logout to the right */}
        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '16px' }}>

          <span style={{ fontSize: '14px', opacity: 0.85 }}>
            Hi, {user.username}
          </span>

          <button
            onClick={handleLogout}
            style={{
              padding: '8px 18px',
              backgroundColor: 'rgba(255,255,255,0.15)',
              color: 'white',
              border: '1px solid rgba(255,255,255,0.4)',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '600',
              borderRadius: '6px'
            }}
          >
            Logout
          </button>

        </div>

      </div>

      {/* Page Content */}
      {currentPage === 'home' && <Home token={user.token} />}
      {currentPage === 'compare' && <ResumeComparison token={user.token} />}
      {currentPage === 'history' && <History token={user.token} />}

    </div>
  )
}

export default App
