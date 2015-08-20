var Results = React.createClass({
    getInitialState: function() {
        return({"data": {}});
    },
    render: function() {
        // TODO: convert to list of objects
        var tiles = [['tree', this.props.data["gene"], "Gene tree"],
                     ['tree', this.props.data["species"], "Species tree"],
                     ['tree', this.props.data["mapping"], "Mapping"],
                     ['scenarios', this.props.data["scenarios"], "Scenarios"]];
        var tiles = tiles.map(function(tile){
            return (
                <ResultTile kind={tile[0]} content={tile[1]} title={tile[2]} />
            );
        });
        return ( <div className="row"> {tiles} </div> )
    }
});

var ResultTile = React.createClass({
    renderChild: function(){
        // Better solution?
        if (this.props.kind == 'tree'){
            return (<TreePic svg={this.props.content} />);
        } else if (this.props.kind == 'scenarios'){
            return (<ScenarioList content={this.props.content} />);
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
            <div dangerouslySetInnerHTML={{__html: this.props.svg}}></div>
        );
    }
});
var ScenarioList = React.createClass({
    renderScenario: function(scenario){
        return (<Scenario noted={scenario} />);
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
    render: function(){
        var embedding = this.showEmbedding()
        return (
            <div className="jesym">
            <tr>
                <td>{this.props.noted}</td>
                <td> <div className="small info btn">
                    <button className="slim" onClick={this.drawEmbedding}> Draw </button>
                </div> </td>
            </tr>
            {embedding}
            </div>
        );
    },
    drawEmbedding: function(){
        // request picture
        // write to this.state.picture
    },
    showEmbedding: function(){
        if (this.state.picture){
            return (
                <tr>
                <div dangerouslySetInnerHTML={{__html: this.state.picture}}></div>
                </tr>
            );
        }
    }
});
