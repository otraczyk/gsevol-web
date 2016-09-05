var UnrootedApp = React.createClass({
  mixins: [App],
  apiUrl: '/api/unrooted/',
  renderResults: function() {
    return <UnrootedResults data={this.state.data} />;
  },
  componentDidMount: function() {
    if (this.state.params.cost) {
      document.getElementById(this.state.params.cost).checked = true;
    }
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
    var tiles = [['unrooted', this.props.data["unrooted"], "Unrooted gene tree"],
                 ['species', this.props.data["species"], "Species tree"],
                 ['rootings', this.props.data["rootings"], "Optimal rootings"]
          ];
    var tiles = tiles.map(function(tile){
      return (
        <ResultTile kind={tile[0]} content={tile[1] || {}} title={tile[2]} />
      );
    });
    return <div className="row">{tiles} </div>;
  }
});
