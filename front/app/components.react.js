var ResultTile = React.createClass({
  render: function() {
    return (
        <TreePic svg={this.props.svg} />
    );
  }
});
var TreePic = React.createClass({
  render: function() {
    return (
        // Simple for now, but e.g. download button should be added
        <div dangerouslySetInnerHTML={{__html: this.props.svg}}></div>
    );
  }
});
