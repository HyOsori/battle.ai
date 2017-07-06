/**
 * Created by mypc on 2017-07-06.
 */


var Sign_in = React.createClass({
    render: function () {

        return (
            <div>

                <form action="/auth/signin" method="POST">
  <div class="form-group">

    <input type="text" name="name" class="form-control" id="exampleInputName" placeholder="name"/>

    <input type="password" name="password" class="form-control" id="exampleInputPassword1" placeholder="password"/>


  <button type="submit" class="btn btn-default">Sign in</button>
  </div>
</form>
            </div>
        );
    }
});

        React.render(
        <Sign_in/>
        ,document.getElementById('sign_in'));
