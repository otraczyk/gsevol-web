var App = {
  getInitialState: function() {
    return {'params': getUrlParams()};
  },
  componentWillMount: function() {
    if (this.state.params){
      var request = jsonPostRequest(this.apiUrl);
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
