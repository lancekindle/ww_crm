"""
Response handling utilities for the Window Wash CRM application.
"""

from flask import jsonify, render_template, request, redirect, url_for


def is_json_request():
    """
    Determine if the current request is expecting a JSON response.
    
    Returns:
        bool: True if the request expects JSON, False otherwise
    """
    return (
        request.headers.get("Accept") == "application/json" 
        or request.content_type == "application/json"
    )


def render_response(template_name, json_data, status_code=200, **template_args):
    """
    Render a response based on the request content type.
    
    Args:
        template_name (str): The template to render for HTML responses
        json_data (dict or list): The data to return for JSON responses
        status_code (int, optional): HTTP status code to return. Defaults to 200.
        **template_args: Additional arguments to pass to the template
        
    Returns:
        Response: Either a JSON response or a rendered template
    """
    if is_json_request():
        return jsonify(json_data), status_code
    return render_template(template_name, **template_args), status_code


def created_response(entity, template_name=None, redirect_endpoint=None, **template_args):
    """
    Return an appropriate response for a resource creation.
    
    Args:
        entity (dict): The created entity data for JSON responses
        template_name (str, optional): Template to render for HTML responses
        redirect_endpoint (str, optional): Endpoint to redirect to for HTML responses
        **template_args: Additional arguments to pass to the template
        
    Returns:
        Response: Either a JSON response, a redirect, or a rendered template
    """
    if is_json_request():
        return jsonify(entity), 201
    
    if redirect_endpoint:
        return redirect(url_for(redirect_endpoint))
    
    return render_template(template_name, **template_args), 201


def no_content_response():
    """
    Return a 204 No Content response.
    
    Returns:
        tuple: Empty string and 204 status code
    """
    return "", 204