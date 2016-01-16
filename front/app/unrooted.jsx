var UnrootedApp = React.createClass({
    getInitialState: function() {
        console.log(getUrlParams());
        return {'params': getUrlParams()};
    },
    componentWillMount: function() {
        if (this.state.params){
            var request = jsonPostRequest('/api/unrooted/');
            var params = this.state.params;
            request.onload = function() {
                console.log(request.responseText);
              if (request.status == 200) {
                var response = JSON.parse(request.responseText);
                this.setState(_.merge({}, this.state, {'data': response}));
              } else {
                this.setState(_.merge({}, this.state, {'error': request.responseText}));
              }
            }.bind(this)
            request.send(JSON.stringify(params));
        }
    },
    render: function() {
        if (this.state.data){
            return <UnrootedResults data={this.state.data} />;
        } else if (this.state.error) {
            return <Error message={this.state.error} />;
        } else {
            return <div></div>;
        }
    }
});

var UnrootedResults = React.createClass({
    getInitialState: function() {
        return {
          data: {}
        };
      },
    render: function() {
        // TODO: convert to list of objects
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
