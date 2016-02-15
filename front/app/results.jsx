var ResultTile = React.createClass({
  renderChild: function(){
    // Better solution?
    if (this.props.kind == 'tree'){
      return <TreePic svg={this.props.content} />;
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
  render: function() {
    return (
      // Simple for now, but e.g. download button should be added
      <div>
      {this.props.noted}
      <div dangerouslySetInnerHTML={{__html: this.props.svg}}></div>
      </div>
    );
  }
});

var Scenario = React.createClass({
  render: function() {
    return (
      // Simple for now, but e.g. download button should be added
      <div>
      {this.props.noted}
      <div className="scen-cost">
        Duplications: {this.props.cost.dups}<br/>
        Losses: {this.props.cost.losses}
      </div>
      <div dangerouslySetInnerHTML={{__html: this.props.svg}}></div>
      </div>
    );
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
