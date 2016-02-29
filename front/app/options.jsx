var Options = React.createClass({
  getInitialState: function() {
    return {'options': []};
  },
  componentWillMount: function() {
    // Fetch available props for current kind of tree to be styled
    jsonRequestPromise('/api/options', {'kind': this.props.kind}, 'GET')
      .then(function(results) {
        this.setState({'options': results});
      }.bind(this));
  },
  renderFormField: function(field) {
    return (
      <div>
          <label for="field">{field.label} </label>
          <input type={field.input} name={field.name}
              value={field.default}  />
      </div>
      );
  },
  renderForm: function(){
    var fields = this.state.options.map(this.renderFormField);
    return (
      <form id="options-form" method="get" action="">
      <div className="pure-control-group">
        {fields}
        <button type="submit" value="Submit">Submit</button>
      </div>
      </form>
      )
  },
  hideSidebar: function(){
    document.getElementById('options').style.visibility = "hidden";
  },
  render: function() {
    var form = this.renderForm()
    return (<div>
      <button className="fold" onClick={this.hideSidebar}> X </button>
      <h3> Style options - {this.props.kind} </h3>
        {form}
      </div>);
  }
});
