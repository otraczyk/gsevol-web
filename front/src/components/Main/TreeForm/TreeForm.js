import React, { Component, PropTypes } from 'react';
import cx from 'classnames';
import config from '../../../config.js';
import fetch from '../../../core/fetch';
import s from './TreeForm.scss';
import withStyles from '../../../decorators/withStyles';
import Link from '../../Utils/Link';

@withStyles(s)
class TreeForm extends Component {

  static propTypes = {
    className: PropTypes.string,
  };

  render() {
    return (
      <form id="input-form" method="post" className="pure-form pure-form-aligned">
        <div className="pure-control-group">
            <label htmlFor="gene">Gene tree</label>
            <input type="text" ref="gene" className="pure-input"
                value="default_gene" id="gene" />
        </div>
        <div className="pure-control-group">
        <label htmlFor="species">Species tree</label>
        <input type="text" ref="species" className="pure-input"
            value="default_species" id="species" />
            <button type="submit" value="Submit" className="pure-button"
              onClick={this.submitForm}>Submit</button>
        </div>
      </form>
    );
  }

  async submitForm() {
    console.log(config.backendUrl + 'draw/');
    // var results = await fetch(config.backendUrl + 'draw/', {
    //   method: 'post',
    //   headers: {
    //     'Accept': 'application/json',
    //     'Content-Type': 'application/json'
    //   },
    //   body: JSON.stringify({
    //     gene: this.refs.gene,
    //     species: this.refs.species
    //   })
    // })

    console.log(results);
  }

}

export default TreeForm;
