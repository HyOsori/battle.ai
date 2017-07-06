
/*
class Login extends React.Component{
    render(){

        let style={
            textAlign: 'center',
            float:'right',
            margin:'20px',
            width:'30vw'
        }
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
}*/
//
var Sign_in = React.createClass({
    render:function () {
        return(
            <div>
                <h1>ㅗㅑ</h1>>
                <button id="sign_in"style="float:right;margin:20px"type="button" class="btn btn-default navbar-btn">Sign in</button>
            </div>
        );

    }

});
var Sign_up = React.createClass({
    render:function () {
        return(

            <h1>안녕녕</h1>
       );

    }

});
React.render(<Sign_in/>,document.getElementById('sign_in'));

React.render(<Sign_up/>,document.getElementById('sign_up'));
