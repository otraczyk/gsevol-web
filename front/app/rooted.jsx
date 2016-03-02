var RootedApp = React.createClass({
  mixins: [App],
  apiUrl: '/api/draw/',
  renderResults: function() {
    return <Results data={this.state.data} />;
  },
  render: function(){
    return this.baseRender();
  }
});

var Results = React.createClass({
  getInitialState: function() {
    return {
      data: {}
    };
  },
  render: function() {
    // TODO: convert to list of objects
    var tiles = [
      ['gene', this.props.data["gene"], "Gene tree"],
      ['species', this.props.data["species"], "Species tree"],
      ['mapping', this.props.data["mapping"], "LCA Mapping"],
      ['scenario', this.props.data.optscen, "Optimal evolutionary scenario in duplication-loss model"],
      ['scenarios', this.props.data["scenarios"], "All scenarios"]
    ];
    if (this.props.data["gene"] && this.props.data["species"]) {
      tiles.push(['button', {text: "Open diagram", resType: "diagram"}, 'Diagram']);
    }
    var tiles = tiles.map(function(tile){
      return <ResultTile kind={tile[0]} content={tile[1]} title={tile[2]} />;
    });
    return <div className="row">{tiles} </div>;
  }
});
