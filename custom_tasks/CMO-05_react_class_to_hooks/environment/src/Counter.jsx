import React from 'react'
class Counter extends React.Component {
  constructor(p){super(p); this.state={count:0}}
  componentDidMount(){ console.log('mounted') }
  render(){ return (
    <div>
      <span>{this.state.count}</span>
      <button onClick={() => this.setState(s=>({count:s.count+1}))}>+</button>
    </div>) }
}
export default Counter
