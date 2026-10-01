"""Local preview server for site/ that renders site/404.html for missing pages,
the way Netlify does. Usage: python tools/serve.py [port]"""
import http.server, pathlib, sys

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE), **kwargs)

    def send_error(self, code, message=None, explain=None):
        page = SITE / "404.html"
        if code != 404 or not page.exists():
            return super().send_error(code, message, explain)
        body = page.read_bytes()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(f"Serving site/ on http://localhost:{port}")
    http.server.ThreadingHTTPServer(("", port), Handler).serve_forever()
