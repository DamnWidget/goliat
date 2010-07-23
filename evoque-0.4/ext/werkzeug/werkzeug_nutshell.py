#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path
from werkzeug import BaseRequest, BaseResponse, \
        SharedDataMiddleware, responder
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException
from evoque.domain import Domain

# path for this file's folder 
# used as root for default template collection
root_path = path.abspath(path.dirname(__file__))

# create an evoque template domain (and default collection) 
domain = Domain(root_path)

# create the URL map. The endpoints are template names without the 
# .html extension, to be rendered by the `dispatch_request` function.
url_map = Map([
    Rule('/', endpoint='index'),
    Rule('/hello/', defaults={'name': 'World'}, endpoint='say_hello'),
    Rule('/hello/<name>', endpoint='say_hello'),
    Rule('/shared/<file>', endpoint='shared', build_only=True)
])


def dispatch_request(environ, start_response):
    """
    A simple dispatch function that (if decorated with responder) 
    is the complete WSGI application that does the template  
    rendering and error handling.
    """
    # first we bind the url map to the current request
    adapter = url_map.bind_to_environ(environ)
    # then we wrap all the calls in a try/except for HTTP exceptions
    try:
        # get the endpoint and the values (variable or parts)
        # of the adapter.  If the match fails it raises a NotFound
        # exception which is a HTTPException which we catch
        endpoint, values = adapter.match()
        
        # create a new request object for the incoming WSGI environ
        request = BaseRequest(environ)
        
        # create an empty response object with the correct mimetype.
        response = BaseResponse(mimetype='text/html')
        
        # get the template and render it. Pass some useful stuff to 
        # the template (request and response objects, the current  
        # url endpoint, the url values and a url_for function which 
        # can be used to generate urls
        template = domain.get_template(endpoint + '.html')
        response.write(template.evoque(
            request=request,
            response=response,
            endpoint=endpoint,
            url_for=lambda e, **v: adapter.build(e, v),
            url_values=values
        ))
        
        # return the response
        return response
    
    except HTTPException, e:
        # if an http exception is caught we can return it as  
        # response because those exceptions render standard error 
        # messages under wsgi
        return e


# finish the wsgi application by wrapping it in a middleware that 
# serves static files in the shared folder and wrap the dispatch 
# function in a responder so that the return value is called as 
# wsgi application.
application = SharedDataMiddleware(responder(dispatch_request), {
    '/shared':  path.join(root_path, 'shared')
})


# if the script is called from the command line start the 
# application with the development server on localhost:4000
if __name__ == '__main__':
    from werkzeug import run_simple
    run_simple('localhost', 4000, application)
