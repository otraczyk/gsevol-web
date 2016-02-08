var ListItem = React.createClass({
  getInitialState: function(){
    return ({"picture": null});
  },
  showButton: function(){
    if (!this.state.picture){
      return (
        <td>
         <div className="small info btn">
          <button className="slim" onClick={this.drawPicture}> Draw </button>
        </div>
        </td>
      );
    }
  },
  render: function(){
    var picture = this.showPicture()
    var button = this.showButton()
    return (
      <tr>
        <td>{this.props.noted}
          {picture}
        </td>
        {button}
      </tr>
    );
  },
  drawPicture: function(){
    this.props.pictureRequest(this.props.noted)
      .then(function(data){
          this.setState({picture: data});
        }.bind(this)
      );
  },
  showPicture: function(){
    if (this.state.picture){
      return (
        <TreePic svg={this.state.picture} />
      );
    }
  }
});

var List = {
  renderItem: function(item){
    return <ListItem noted={item} pictureRequest={this.pictureRequest} />;
  },
  baseRender: function() {
    var scenRows = this.props.content.map(this.renderItem);
    return (
      <table><tbody>
        {scenRows}
      </tbody></table>
    );
  }
};

var ScenarioList = React.createClass({
  mixins: [List],
  pictureRequest: function(item){
    var params = {"scenario": item,
                  "species": document.getElementById("species").value};
    return JsonRequestPromise('/api/embedding/', params, 'POST');
  },
  render: function() {
    return this.baseRender();
  }
});

var RootingList = React.createClass({
  mixins: [List],
  pictureRequest: function(item){
    return JsonRequestPromise('/api/draw_single/', item, 'POST');
  },
  render: function() {
    return this.baseRender();
  }
});
