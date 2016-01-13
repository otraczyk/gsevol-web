var Results = React.createClass({
    getInitialState: function() {
        return {
          data: {}
        };
      },
    render: function() {
        // TODO: convert to list of objects
        var tiles = [['tree', this.props.data["gene"], "Gene tree"],
                     ['tree', this.props.data["species"], "Species tree"],
                     ['tree', this.props.data["mapping"], "Mapping"],
                     ['scenario', this.props.data.optscen, "Optimal evolutionary scenario"],
                     ['button', {text: "Open diagram", resType: "diagram"}, 'Diagram'],
                     ['scenarios', this.props.data["scenarios"], "All scenarios"]
                    ];
        var tiles = tiles.map(function(tile){
            return (
                <ResultTile kind={tile[0]} content={tile[1]} title={tile[2]} />
            );
        });
        return <div className="row">{tiles} </div>;
    }
});

var ResultTile = React.createClass({
    renderChild: function(){
        // Better solution?
        if (this.props.kind == 'tree'){
            return <TreePic svg={this.props.content} />;
        } else if (this.props.kind == 'scenarios'){
            return <ScenarioList content={this.props.content} />;
        } else if (this.props.kind == 'scenario'){
            return <TreePic noted={this.props.content.scen} svg={this.props.content.pic} />;
        } else if (this.props.kind == 'button'){
            return (
                <ButtonTile text={this.props.content.text}
                    resType={this.props.content.resType} />
                );
        }
    },
    render: function() {
        if (this.props.content){
            var child = this.renderChild()
            return (
                <div className="result-tile">
                    <div className="title"> {this.props.title} </div>
                    {child}
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
            <div>
            {this.props.noted}
            <div dangerouslySetInnerHTML={{__html: this.props.svg}}></div>
            </div>
        );
    }
});

var ScenarioList = React.createClass({
    renderScenario: function(scenario){
        return <Scenario noted={scenario} />;
    },
    render: function() {
        var scenRows = this.props.content.map(this.renderScenario);
        return (
            <table><tbody>
                {scenRows}
            </tbody></table>
        );
    }
});
var Scenario = React.createClass({
    getInitialState: function(){
        return ({"picture": null});
    },
    showButton: function(){
        if (!this.state.picture){
            return (
                <td>
                 <div className="small info btn">
                    <button className="slim" onClick={this.drawEmbedding}> Draw </button>
                </div>
                </td>
                );
        }
    },
    render: function(){
        var embedding = this.showEmbedding()
        var button = this.showButton()
        return (
            <tr>
                <td>{this.props.noted}
                    {embedding}
                </td>
                {button}
            </tr>
        );
    },
    drawEmbedding: function(){
        var request = jsonPostRequest('/api/embedding/')
        var params = {"scenario": this.props.noted,
                      "species": document.getElementById("species").value};
        request.onload = function() {
          if (request.status == 200){
            this.setState({picture: JSON.parse(request.responseText)});
          } else {
            console.log(request.responseText);
          }
        }.bind(this);
        request.send(JSON.stringify(params))
    },
    showEmbedding: function(){
        if (this.state.picture){
            return (
                <TreePic svg={this.state.picture} />
            );
        }
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
})
