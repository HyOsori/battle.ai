/**
 * Created by mypc on 2017-07-06.
 */

var Body = React.createClass({
    render: function(){
        let style={
            paddingTop:'23px'
        }
        return(
            <div style={style}>
            </div>
        );
    }
})
var Sign_in = React.createClass({
    render: function () {
           let style={
            position:'fixed',
            width:'100%',
            height:'70px',
            backgroundColor:'#009688',
            boxShadow:'0 1px 0 rgba(0,0,0,.10196078)',
               padding:'10px',
               zIndex:'999'

        }
        let style1={
           float:'right'
        }

        return (
            <div style={style} >
                <form className="form-inline" action="/auth/signin" method="POST" style={style1}>
                  <div className="form-group">

                    <input type="text" name="name" className="form-control" id="exampleInputName" placeholder="name"/>



                    <input type="password" name="password" className="form-control" id="exampleInputPassword1" placeholder="password"/>
                    </div>
                  <button type="submit" className="btn btn-default">Sign in</button>

                </form>

            </div>
        );
    }
});
var Footer = React.createClass({
    render: function(){
        let style={
            width:'100%',
            position: 'fixed',
            height: '100px',
            bottom:0,
            float:'center',
            backgroundColor:'#EEEEEE',
            fontSize:'15px',
            fontColor:'#424242',
            padding:'10px',
            fontFamily:'inherit'
        }
        return(
            <div style={style}>
                <div >
                <p>LICENSE</p>
                <p>OPEN SOURCE</p>
                <p>GITHUB LINK</p>
                </div>
                </div>);
    }
});
        React.render(
        <Sign_in/>
        ,document.getElementById('sign_in'));
             React.render(
        <Body/>
        ,document.getElementById('body'));
          React.render(
        <Footer/>
        ,document.getElementById('footer'));
