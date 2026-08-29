import React, { useState, useEffect } from 'react'
export default function Counter() {
  const [count, setCount] = useState(0)
  useEffect(() => { console.log('mounted') }, [])
  return (
    <div>
      <span>{count}</span>
      <button onClick={() => setCount(c => c + 1)}>+</button>
    </div>)
}
