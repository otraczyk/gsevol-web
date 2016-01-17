var UnrootedApp = React.createClass({
  mixins: [App],
  apiUrl: '/api/unrooted/',
  renderResults: function() {
    return <UnrootedResults data={this.state.data} />;
  },
  render: function(){
    return this.baseRender();
  }
});

var UnrootedResults = React.createClass({
  getInitialState: function() {
    return {
      data: {}
    };
  },
  render: function() {
    var tiles = [['tree', this.props.data["unrooted"], "Unrooted gene tree"],
          ];
    var tiles = tiles.map(function(tile){
      return (
        <ResultTile kind={tile[0]} content={tile[1]} title={tile[2]} />
      );
    });
    return <div className="row">{tiles} </div>;
  }
});
