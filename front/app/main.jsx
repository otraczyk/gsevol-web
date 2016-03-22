var App = {
  getInitialState: function() {
    return {'params': getUrlParams()};
  },
  openSocket: function(){
    // We neet the socket open before any results can come, or they'll be lost.
    return new Promise(function(resolve, reject) {
      var onSocketOpen = function() {
        console.log("socket opened");
        this.requestResults();
      }.bind(this);
      var onSocketMessage = function(data) {
        data = JSON.parse(data)
        console.log("Received: " + Object.keys(data));
        if ("error" in data){
          this.setState(_.merge({}, this.state, data));
        } else if (this.state.error) {
            this.setState({"error": null});
        }
        this.setState(_.merge({}, this.state, {'data': data}));
      }.bind(this);
      var uri = 'ws://' + location.host + '/ws/' + location.search.slice(1)
        + '?subscribe-broadcast&publish-broadcast&echo';
      socket = new WS4Redis({
        uri: uri,
        connected: onSocketOpen,
        receive_message: onSocketMessage,
      });
      this.socket = socket;
      resolve();
    }.bind(this));
  },
  requestResults: function() {
    if (this.state.params){
      jsonRequestPromise(this.apiUrl, this.state.params, 'POST')
        .catch(function(response) {
            this.setState(_.merge({}, this.state, {'error': response.responseText}));
          }.bind(this));
    }
  },
  componentWillMount: function() {
    this.openSocket();
  },
  baseRender: function() {
    if (this.state.data && this.state.error){
      return <div> <Error message={this.state.error} /> {this.renderResults()} </div>
    }
    else if (this.state.error) {
      return <Error message={this.state.error} />;
    }
    else if (this.state.data){
      return this.renderResults();
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
  getLink: function(targetPattern) {
    var ret = {link: '', isCurrent: ''};
    if (location.pathname.search(targetPattern) >= 0) {
      ret. link = "#";
      ret.isCurrent = "current";
    } else {
      ret.link = targetPattern + '/' + location.search;
    }
    return ret;
  },
  render: function() {
    var rooted = this.getLink('/rooted');
    var unrooted = this.getLink('/unrooted');
    var scenario = this.getLink('/scenario');
    return (
      <ul>
        <li className={rooted.isCurrent}>
          <a href={rooted.link}> Rooted Tree </a></li>
        <li className={unrooted.isCurrent}>
          <a href={unrooted.link}> Unrooted Tree </a></li>
        <li className={scenario.isCurrent}>
          <a href={scenario.link}> Scenario </a></li>
      </ul>
    );
  }
});
