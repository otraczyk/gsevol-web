var Options = React.createClass({
  mixins: [React.addons.LinkedStateMixin],
  getInitialState: function() {
    return {'options': []};
  },
  componentWillMount: function() {
    this.fetchOptions(this.props.kind);
  },
  componentWillReceiveProps: function(newProps) {
    this.fetchOptions(newProps.kind);
  },
  fetchOptions: function(kind) {
    // Fetch available props for current kind of tree to be styled
    jsonRequestPromise('/api/options/', {'kind': kind}, 'POST')
      .then(function(results) {
        this.setState({'options': results});
        var conf = {}
        _.each(results, function(opt) {
            conf[opt.name] = opt.default;
          });
        this.setState(conf);
      }.bind(this))
      .catch(function(error){
        this.setState({'options': []});
      }.bind(this));
  },
  renderFormField: function(field) {
    var name = field.name;
    if (field.input === "checkbox") {
      var input = <input type={field.input} name={name}
            checkedLink={this.linkState(name)}
            onClick={this.handleFieldChange} />
    } else if (field.input === 'dropdown'){
      var options = _.map(field.scope, function(variant){
        return <option value={variant[0]}>{variant[1]}</option>
      });
      var input = (<select name={field.name} valueLink={this.linkState(name)}>
                      {options}
                  </select>);
    } else {
      var input = <input type={field.input} name={name}
            valueLink={this.linkState(name)}
            onClick={this.handleFieldChange} />
    }
    return (
      <div className="pure-control-group">
          <label htlmFor="field">{field.label} </label>
          {input}
      </div>
      );
  },
  handleFieldChange: function(event) {
    event.stopPropagation();  // Avoiding .preventDefault() from form
  },
  renderForm: function() {
    var fields = this.state.options.map(this.renderFormField);
    return (
      <form id="options-form" method="post" onClick={this.pass}>
        {fields}
      <div className="pure-controls">
        <button onClick={this.submit}>Submit</button>
      </div>
      </form>
      )
  },
  hideSidebar: function() {
    document.getElementById('options').style.visibility = "hidden";
  },
  submit: function() {
    var currentConf = {}
    currentConf[this.props.kind] = _.omit(this.state, ["options"]);
    var params = {
      "config": currentConf,
      "kind": this.props.kind
    };
    _.merge(params, getUrlParams())
    jsonRequestPromise('/api/restyle/', params, 'POST')
      .then(function(results){
        console.log(results);
      })
  },
  pass: function(form) {
    form.preventDefault();
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
