var Sign_up = React.createClass({
    render: function () {
        let style = {
            float: 'right',
            marginRight: '100px',
            paddingTop: '10px'
        }
        return (
            <div style={style}>
                <h1>Sign Up</h1>
                <form action="/auth/signup" method="POST" id="react_sign_up">
                    <div className="form-group">
                        <label >Name</label>
                        <input type="text" name="name" className="form-control" id="exampleInputName"
                               placeholder="name"/>
                    </div>
                    <div className="form-group">
                        <label >Password</label>
                        <input type="password" name="password" className="form-control" id="exampleInputPassword1"
                               placeholder="password"/>
                    </div>
                    <div className="form-group">
                        <label >Password confirm</label>
                        <input type="password" name="password_confirm" className="form-control"
                               id="exampleInputPassword2"
                               placeholder="password confirm" title="Please enter the same Password as above"/>
                    </div>
                    <button type="submit" className="btn btn-default navbar-btn">Sign up</button>

                    {console.log(document.getElementById('exampleInputPassword1'))}
                </form>


                { ( (document.getElementById('exampleInputPassword1').valueOf()!==null) ?
                    (( document.getElementById('exampleInputPassword1').valueOf() !== document.getElementById('exampleInputPassword2').valueOf()) ?
                        alert("Passwords Don't Match") : alert('success')) : '')}
                {console.log(document.getElementById('exampleInputPassword1'))}

                {console.log(document.getElementById('exampleInputPassword1')).valueOf()}
            </div>
        );
    }
});

React.render(
    <Sign_up/>
    , document.getElementById('sign_up'));
