do()->
  websocket = ->
    url = 'ws://127.0.0.1:8000/debug'
    ws = new WebSocket(url)

    ws.onclose = ->
      setTimeout ->
        ws = new websocket()
        ws.onopen = ->
          window.location.reload()
        return
      , 1500

    ws.onmessage = (event) ->
      console.log document.webkitHidden
      if document.webkitHidden
        return
      msg = JSON.parse event.data
      if not msg.reload
        return
      path = msg.reload
      console.log path
      list = path.split('.')
      type = list[list.length - 1]

      if ['coffee', 'md', 'jade'].indexOf(type) != -1
        window.location.reload()
      else if type is 'css'
        for el,idx in document.querySelectorAll('link')
          uri = el.href.split('?')[0].split(window.location.origin)[1]
          if path.indexOf(uri) != -1
            setTimeout ()->
              el.href = uri + '?' + Date.now()
            , 500

    return ws

  debug = new websocket()

  debug.onopen = ->
  return
