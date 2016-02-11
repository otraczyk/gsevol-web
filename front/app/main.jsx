var App = {
  getInitialState: function() {
    return {'params': getUrlParams(), 'socket': this.openSocket()};
  },
  openSocket: function(){
    socket = new WebSocket(
      'ws://' + location.host + '/ws/' + location.search.slice(1)
      + '?subscribe-broadcast&publish-broadcast&echo'
    );
    socket.onopen = function() {
        console.log("websocket connected");
    };
    socket.onerror = function(e) {
        console.error(e);
    };
    socket.onclose = function(e) {
        console.log("connection closed");
    }
    socket.onmessage = function(message) {
      console.log("Received: " + message.data);
      this.setState(_.merge({}, this.state, {'data': JSON.parse(message.data)}));
    }.bind(this);
    return socket;
  },
  componentWillMount: function() {
    if (this.state.params){
      jsonRequestPromise(this.apiUrl, this.state.params, 'POST')
        .then(function(response) {
            this.setState(_.merge({}, this.state, {'data': response}));
          }.bind(this))
        .catch(function(response) {
            this.setState(_.merge({}, this.state, {'error': request.responseText}));
          }.bind(this));
    }
  },
  baseRender: function() {
    if (this.state.data){
      return this.renderResults();
    } else if (this.state.error) {
      return <Error message={this.state.error} />;
    } else {
      return <div></div>;
    }
  }
};

var Error = React.createClass({
  render: function() {
    return (
      <li className="danger alert">
        Error processing input: {this.props.message}
      </li>
    );
  }
});

var Nav = React.createClass({
  getLink: function(isTargetCurrent, targetPattern) {
    var ret = {link: '', isCurrent: ''};
    if (isTargetCurrent) {
      ret. link = "#";
      ret.isCurrent = "current";
    } else {
      ret.link = targetPattern + location.search;
    }
    return ret;
  },
  render: function() {
    var onRootedUrl = location.pathname.search('/unrooted/') < 0;
    var rooted = this.getLink(onRootedUrl, '/rooted/');
    var unrooted = this.getLink(!onRootedUrl, '/unrooted/');
    return (
      <ul>
        <li className={rooted.isCurrent}>
          <a href={rooted.link}> Rooted Tree </a></li>
        <li className={unrooted.isCurrent}>
          <a href={unrooted.link}> Unrooted Tree </a></li>
      </ul>
    );
  }
});
