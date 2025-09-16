from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.utils.deprecation import MiddlewareMixin
import os
import mimetypes

@never_cache
@require_http_methods(["GET"])
def serve_media_with_cors(request, path):
    """
    Serve media files with proper CORS headers to allow cross-origin access.
    This is especially important when using ngrok or other tunnel services.
    """
    # Build the full file path
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Check if file exists
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise Http404("File not found")
    
    # Get the file's MIME type
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    # Read the file
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
    except IOError:
        raise Http404("File not accessible")
    
    # Create response with CORS headers
    response = HttpResponse(content, content_type=content_type)
    
    # Add CORS headers
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'ngrok-skip-browser-warning, User-Agent'
    response['Access-Control-Expose-Headers'] = 'content-type, content-length, cache-control, expires, last-modified, etag'
    
    # Add cache headers
    response['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
    
    return response
