function UploadForm({
  setResume,
  setJobDescription,
  handleSubmit
}) {

  return (

    <div>

      <div
        style={{
          marginBottom: '20px'
        }}
      >

        <input
          type="file"
          onChange={(e) => setResume(e.target.files[0])}
          style={{
            padding: '10px'
          }}
        />

      </div>

      <textarea
        rows="12"
        cols="80"
        placeholder="Paste Job Description Here..."
        onChange={(e) => setJobDescription(e.target.value)}
        style={{
          width: '100%',
          padding: '15px',
          borderRadius: '10px',
          border: '1px solid #d1d5db',
          fontSize: '15px',
          resize: 'none',
          outline: 'none',
          marginBottom: '20px'
        }}
      />

      <button
        onClick={handleSubmit}
        style={{
          backgroundColor: '#2563eb',
          color: 'white',
          padding: '12px 25px',
          border: 'none',
          borderRadius: '10px',
          fontSize: '16px',
          fontWeight: 'bold',
          cursor: 'pointer'
        }}
      >
        Analyze Resume
      </button>

    </div>
  )
}

export default UploadForm