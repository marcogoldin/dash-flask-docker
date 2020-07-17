from werkzeug.middleware.dispatcher import DispatcherMiddleware

from flask_app import server, dash_app1, dash_app2

application = DispatcherMiddleware(server, {
    '/app1': dash_app1.server,
    '/app2': dash_app2.server,
})

