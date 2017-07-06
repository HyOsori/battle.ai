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
    render: function () {
        let style = {
            float: 'right',
            margin: '20px'
        }
        return (
            <div>
                <button id="sign_in" type="button" class="btn btn-default navbar-btn">Sign in</button>
            </div>
        );

    }

});
var Sign_up = React.createClass({
    render: function () {

        return (
            <div>
                <h1>Sign Up</h1>
                <form action="/auth/signup" method="POST">
                    <div class="form-group">
                        <label for="exampleInputName">Name</label>
                        <input type="text" name="name" class="form-control" id="exampleInputName" placeholder="name"/>
                    </div>
                    <div class="form-group">
                        <label for="exampleInputPassword1">Password</label>
                        <input type="password" name="password" class="form-control" id="exampleInputPassword1"
                               placeholder="password"/>
                    </div>
                    <div class="form-group">
                        <label for="exampleInputPassword2">Password confirm</label>
                        <input type="password" name="password_confirm" class="form-control" id="exampleInputPassword2"
                               placeholder="password confirm"/>
                    </div>
                     {document.getElementById('exampleInputPassword1').value==document.getElementById('exampleInputPassword1').value?'TRUE':'FALSE'}
                    <button type="submit" class="btn btn-default navbar-btn">Sign up</button>
                </form>

            </div>
        );
    }
});

        React.render(
        <Sign_in/>
        ,document.getElementById('sign_in'));
        React.render(
        <Sign_up/>
        ,document.getElementById('sign_up'));
