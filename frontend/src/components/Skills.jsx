function Skills({ title, items }) {

  const isMatched = title.toLowerCase().includes('matched')

  return (

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
          color: isMatched ? '#16a34a' : '#dc2626'
        }}
      >
        {isMatched ? '✅' : '❌'} {title}
      </h2>

      {
        items.length === 0 ? (

          <p>No skills found</p>

        ) : (

          <ul
            style={{
              paddingLeft: '20px'
            }}
          >

            {
              items.map((item, index) => (

                <li
                  key={index}
                  style={{
                    marginBottom: '10px',
                    color: isMatched ? '#15803d' : '#b91c1c',
                    fontWeight: '500',
                    textTransform: 'capitalize'
                  }}
                >
                  {item}
                </li>
              ))
            }

          </ul>
        )
      }

    </div>
  )
}

export default Skills