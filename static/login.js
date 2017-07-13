

var Sign_up = React.createClass({
    render: function () {
        let style={
            float:'right',
            marginRight:'100px',
            paddingTop:'10px',
            className:'form-group',
            

        }

        return (
            <div style={style}>
                <h1>Sign Up</h1>
                <form action="/auth/signup" method="POST">
                    <div className="form-group">
                        <label for="exampleInputName">Name</label>
                        <input type="text" name="name" className="form-control" id="exampleInputName" placeholder="name"/>
                    </div>
                    <div className="form-group">
                        <label for="exampleInputPassword1">Password</label>
                        <input type="password" name="password" className="form-control" id="exampleInputPassword1"
                               placeholder="password"/>
                    </div>
                    <div className="form-group">
                        <label for="exampleInputPassword2">Password confirm</label>
                        <input type="password" name="password_confirm" className="form-control" id="exampleInputPassword2"
                               placeholder="password confirm"/>
                    </div>

                    <button type="submit" className="btn btn-default navbar-btn">Sign up</button>
                </form>

            </div>
        );
    }
});


        React.render(
        <Sign_up/>
        ,document.getElementById('sign_up'));
