import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

class Login extends React.Component{
    render(){
/*
        let style={
            textAlign: 'center',
            float:'right',
            margin:'20px',
            width:'30vw'
        }*/
        return(
           // <div style="{style}"></div>
            <h1>codelab</h1>
        );
    }
}
class App extends React.Component{
  render(){
    return(
    <Login/>
    );
  }
}

ReactDOM.render(<App/>,document.getElementById('sign'));
