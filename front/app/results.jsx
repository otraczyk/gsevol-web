var ResultTile = React.createClass({
  renderChild: function(){
    // Better solution?
    if (_.includes(["gene", "species", "mapping", "unrooted"], this.props.kind)) {
      return <TreePic svg={this.props.content} kind={this.props.kind} />;
    } else if (this.props.kind == 'scenarios'){
      return <ScenarioList content={this.props.content} />;
    } else if (this.props.kind == 'rootings'){
      return <RootingList content={this.props.content} />;
    } else if (this.props.kind == 'scenario'){
      return <Scenario noted={this.props.content.scen}
      svg={this.props.content.pic} cost={this.props.content.cost} />;
    } else if (this.props.kind == 'button'){
      return (
        <ButtonTile text={this.props.content.text}
          resType={this.props.content.resType} />
        );
    }
  },
  render: function() {
    if (this.props.content){
      var child = this.renderChild();
      return (
        <div className="result-tile">
          <div className="title"> {this.props.title} </div>
          {child}
        </div>
      );
    } else {
      return <div></div>;
    }
  }
});
var TreePic = React.createClass({
  getDefaultProps: function() {
    return {
      stylable: true
    };
  },
  renderOptions: function() {
    var opt_comp = React.render(
                React.createElement(Options, {"kind": this.props.kind}),
                document.getElementById('options')
              );
    document.getElementById('options').style.visibility = "visible";
    this.setState({'optionsComp': opt_comp});
  },
  render: function() {
    var styleIcon = ''
    if (this.props.stylable) {
      var styleIcon = <i className="fa fa-cogs"
        onClick={this.renderOptions} title="Stype options"></i>
    }
    return (
      <div>
      {this.props.noted}
      <table className="tree">
      <td className="tree-menu">
        {this.props.otherOptions}
        <i className="fa fa-download" onClick={this.renderOptions} title="Download"></i><br/>
        {styleIcon}
      </td>
      <td dangerouslySetInnerHTML={{__html: this.props.svg}}></td>
      </table>
      </div>
    );
  }
});

var Scenario = React.createClass({
  render: function() {
    var costs = (<div> Duplications: {this.props.cost.dups}<br/>
                      Losses: {this.props.cost.losses}
                </div>)
    return <TreePic svg={this.props.svg} otherOptions={costs}  noted={this.props.noted} kind="scenario"/>;
  }
});

var ButtonTile = React.createClass({
  render: function(){
    var url = location.origin + location.pathname + 'diagram/' + location.search;
    return (
      <div className="info btn"> <a href={url} target="blank">
        <button className="slim"> {this.props.text} </button>
      </a> </div>
      );
  }
});
