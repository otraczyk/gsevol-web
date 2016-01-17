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
