var ScenarioApp = React.createClass({
  mixins: [App],
  apiUrl: '/api/scenario/',
  renderResults: function() {
    return <ScenarioResults data={this.state.data} />;
  },
  render: function() {
    return this.baseRender();
  }
});

var ScenarioResults = React.createClass({
  getInitialState: function() {
    return {
      data: {}
    };
  },
  render: function() {
    var tiles = [['scenario', this.props.data["scenario"], "Scenario"],
                 ['tree', this.props.data["species"], "Species tree"]
          ];
    var tiles = tiles.map(function(tile){
      return (
        <ResultTile kind={tile[0]} content={tile[1]} title={tile[2]} />
      );
    });
    return <div className="row">{tiles} </div>;
  }
});
