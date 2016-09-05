var DiagramApp = React.createClass({
  mixins: [App],
  apiUrl: '/api/diagram/',
  renderResults: function() {
    return <TreePic svg={this.state.data.diagram} kind="diagram" />;
  },
  render: function(){
    return this.baseRender();
  }
});
