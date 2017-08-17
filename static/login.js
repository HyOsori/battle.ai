var Sign_up = React.createClass({
    getInitialState: function () {
        return {
            name: '',
            password: '',
            password_confirm: ''
        };
    },
    loginSubmit() {
        if (this.state.password !== '') {
            if (this.state.password === this.state.password_confirm) {
                return true;
            } else {
                alert("비밀번호가 일치하지 않습니다.");
            }
        } else {
            alert("비밀번호를 입력해주세요.")
        }
        return false;
    },
    handleChange: function (e) {
        let nextState = {};
        if (typeof e !== 'object') return ;
        nextState[e.target.name] = e.target.value;
        this.setState(nextState);

    },
    render: function () {
        let style = {
            float: 'right',
            marginRight: '200px',
            paddingTop: '100px',
            width:'20%',
        }

        return (
            <div style={style}>
                <h1>Sign Up</h1>

                <form action="/auth/signup" method="POST" id="react_sign_up" onSubmit={this.loginSubmit}>
                    <div className="form-group">
                        <label >Name</label>
                        <input type="text" name="name" className="form-control" id="exampleInputName" value={this.state.name} placeholder="name" onChange={this.handleChange}/>
                    </div>
                    <div className="form-group">
                        <label >Password</label>
                        <input type="password" name="password" className="form-control" id="exampleInputPassword1" value={this.state.password}
                               placeholder="password" onChange={this.handleChange}/>
                    </div>
                    <div className="form-group">
                        <label >Password confirm</label>
                        <input type="password" name="password_confirm" className="form-control" value={this.state.password_confirm}
                               id="exampleInputPassword2"
                               placeholder="password confirm" title="Please enter the same Password as above" onChange={this.handleChange}/>
                    </div>
                    <button type="submit" className="btn btn-default navbar-btn">Sign up</button>

                </form>


            </div>
        );
    }
});

React.render(
    <Sign_up/>
    , document.getElementById('sign_up'));