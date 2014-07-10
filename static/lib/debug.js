// Generated by CoffeeScript 1.6.3
(function() {
  (function() {
    var debug, websocket;
    websocket = function() {
      var url, ws;
      url = 'ws://127.0.0.1:8000/debug';
      ws = new WebSocket(url);
      ws.onclose = function() {
        return setTimeout(function() {
          ws = new websocket();
          ws.onopen = function() {
            return window.location.reload();
          };
        }, 1500);
      };
      ws.onmessage = function(event) {
        var el, idx, list, msg, path, type, uri, _i, _len, _ref, _results;
        console.log(document.webkitHidden);
        if (document.webkitHidden) {
          return;
        }
        msg = JSON.parse(event.data);
        if (!msg.reload) {
          return;
        }
        path = msg.reload;
        console.log(path);
        list = path.split('.');
        type = list[list.length - 1];
        if (['coffee', 'md', 'jade'].indexOf(type) !== -1) {
          return window.location.reload();
        } else if (type === 'css') {
          _ref = document.querySelectorAll('link');
          _results = [];
          for (idx = _i = 0, _len = _ref.length; _i < _len; idx = ++_i) {
            el = _ref[idx];
            uri = el.href.split('?')[0].split(window.location.origin)[1];
            if (path.indexOf(uri) !== -1) {
              _results.push(setTimeout(function() {
                return el.href = uri + '?' + Date.now();
              }, 500));
            } else {
              _results.push(void 0);
            }
          }
          return _results;
        }
      };
      return ws;
    };
    debug = new websocket();
    debug.onopen = function() {};
  })();

}).call(this);

/*
//@ sourceMappingURL=debug.map
*/