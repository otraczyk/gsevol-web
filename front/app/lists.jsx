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
    var picture = this.showPicture();
    var button = this.showButton();
    var additional = this.props.showAdditional(this.props.noted);
    return (
      <tr>
        <td>{this.props.noted}
          {picture}
        </td>
        {button}
        {additional}
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
    return ( <ListItem noted={item} pictureRequest={this.pictureRequest}
            showAdditional={this.showAdditional} />);
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
    return jsonRequestPromise('/api/embedding/', params, 'POST');
  },
  showAdditional: function(item) {
    var scenarioLink = '/scenario/?scenario=' + item
        + "&species=" + document.getElementById("species").value;
    return (
      <td>
       <div className="small info btn">
         <a href={scenarioLink}>
          <button className="slim"> Edit scenario </button>
         </a>
      </div>
      </td>
    )
  },
  render: function() {
    return this.baseRender();
  }
});

var RootingList = React.createClass({
  mixins: [List],
  pictureRequest: function(item){
    return jsonRequestPromise('/api/draw_single/', item, 'POST');
  },
  showAdditional: function(item) {
    var rootingLink = '/rooted/?gene=' + item
        + "&species=" + document.getElementById("species").value;
    return (
      <td>
       <div className="small info btn">
         <a href={rootingLink}>
          <button className="slim"> Edit rooting </button>
         </a>
      </div>
      </td>
    )
  },
  render: function() {
    return this.baseRender();
  }
});
