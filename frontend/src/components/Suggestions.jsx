function Suggestions({ suggestions }) {

  return (

    <div
      style={{
        backgroundColor: '#f8fafc',
        padding: '20px',
        borderRadius: '12px',
        boxShadow: '0px 2px 10px rgba(0,0,0,0.08)'
      }}
    >

      <h2
        style={{
          marginBottom: '20px'
        }}
      >
        💡 Suggestions
      </h2>

      {
        suggestions.map((item, index) => (

          <div
            key={index}
            style={{
              backgroundColor: 'white',
              padding: '15px',
              borderRadius: '10px',
              marginBottom: '12px',
              borderLeft: '5px solid #2563eb'
            }}
          >
            {item}
          </div>
        ))
      }

    </div>
  )
}

export default Suggestions