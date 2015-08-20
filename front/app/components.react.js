var Results = React.createClass({
    getInitialState: function() {
        return({"data": {}});
    },
    render: function() {
        var treeTiles = [[this.props.data["gene"], "Gene tree"],
                         [this.props.data["species"], "Species tree"],
                         [this.props.data["mapping"], "Mapping"]];
        var tiles = treeTiles.map(function(tile){
            return (
                <TreeTile svg={tile[0]} title={tile[1]} />
            );
        });
        return ( <div class="row"> {tiles} </div> )
    }
});

var TreeTile = React.createClass({
  render: function() {
    if (this.props.svg){
        return (
            <div className="two column result-tile">
                <div className="title"> {this.props.title} </div>
                <TreePic svg={this.props.svg} />
            </div>
        );
    } else {
        return (<div></div>);
    }
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
