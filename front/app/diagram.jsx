var DiagramApp = React.createClass({
  mixins: [App],
  apiUrl: '/api/diagram/',
  getInitialState: function () {
    return {data: null};
  },
  renderResults: function() {
    return <TreePic svg={this.state.data.diagram} kind="diagram" />;
  },
  render: function(){
    return this.baseRender();
  }
});
