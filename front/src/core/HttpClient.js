/*! React Starter Kit | MIT License | http://www.reactstarterkit.com/ */

import request from 'superagent';
import Dispatcher from './Dispatcher';
import { canUseDOM } from 'fbjs/lib/ExecutionEnvironment';
import storage from '../utils/storage';

function getUrl(path) {
  if (path.startsWith('http') || canUseDOM) {
    return path;
  }

  return process.env.WEBSITE_HOSTNAME ?
    `http://${process.env.WEBSITE_HOSTNAME}${path}` :
    `http://127.0.0.1:${global.server.get('port')}${path}`;
}

const HttpClient = {

  request: (method, path, data) => new Promise((resolve, reject) => {
    Dispatcher.dispatch({
      actionType: 'request-load',
      path: path,
      loading: true
    });

    const req = request[method](getUrl(path))
      .accept('application/json')
      .set('Content-Type', 'application/json')
    ;

    req.withCredentials();
    if (storage.getStoredItem('token').value) {
      req.set('X-CSRFToken', storage.getStoredItem('token'));
    }

    if (data) {
      req.send(JSON.stringify(data));
    }
    req.end((err, res) => {
      if (err) {
        if (err.status === 404) {
          resolve(null);
        } else {
          reject(err);
        }
      } else {
        resolve(res.body);
      }
      Dispatcher.dispatch({
        actionType: 'request-load',
        path: path,
        loading: false
      });
    });
  }),
  post: function post(url, data) {
    return HttpClient.request('post', url, data)
  },
  get: function get(url) {
    return HttpClient.request('get', url)
  },
  fake: function(success, path) {
    return new Promise(function(resolve, reject) {
      Dispatcher.dispatch({
        actionType: 'request-load',
        path: path,
        loading: true
      });
      setTimeout(function() {
        console.log(success)
        if (success) {
          resolve()
        } else {
          reject()
        }
        Dispatcher.dispatch({
          actionType: 'request-load',
          path: path,
          loading: false
        });
      }, Math.random() * 500)
    })
  }
};


export default HttpClient;
