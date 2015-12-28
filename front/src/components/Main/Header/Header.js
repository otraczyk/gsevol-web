/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-2016 Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

import React, { Component } from 'react';
import s from './Header.scss';
import withStyles from '../../../decorators/withStyles';
import Link from '../../Utils/Link';
import Navigation from '../Navigation';

@withStyles(s)
class Header extends Component {

  render() {
    return (
      <div className={s.root}>
        <div className={s.container}>
          <Navigation className={s.nav} />
          <a className={s.brand} href="/" onClick={Link.handleClick}>
            <span className={s.brandTxt}>Gsevol</span>
          </a>
        </div>
      </div>
    );
  }
  // <img src={} width="38" height="38" alt="Gsevol" />

}

export default Header;
