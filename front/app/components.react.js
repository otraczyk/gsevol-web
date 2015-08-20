var ResultTile = React.createClass({
  render: function() {
    return (
        <div className="result-tile">
            <div className="title"> {this.props.title} </div>
            <TreePic svg={this.props.svg} />
        </div>
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
