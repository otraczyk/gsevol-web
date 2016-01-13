var App = React.createClass({
    getInitialState: function() {
        return {'params': getUrlParams()};
    },
    componentWillMount: function() {
        if (this.state.params){
            var request = jsonPostRequest('/api/draw/');
            var params = this.state.params;
            request.onload = function() {
              if (request.status == 200) {
                var response = JSON.parse(request.responseText);
                this.setState(_.merge({}, this.state, {'data': response}));
              } else {
                this.setState(_.merge({}, this.state, {'error': request.responseText}));
              }
            }.bind(this)
            request.send(JSON.stringify(params));
        }
    },
    render: function() {
        if (this.state.data){
            return <Results data={this.state.data} />;
        } else if (this.state.error) {
            return <Error message={this.state.error} />;
        } else {
            return <div></div>;
        }
    }
});

var Error = React.createClass({
    render: function() {
        return (
            <li className="danger alert">
                Error processing input: {this.props.message}
            </li>
        );
    }
})
