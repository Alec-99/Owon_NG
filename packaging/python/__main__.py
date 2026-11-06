"""Offline Owon NG UI launcher; standard-library Python 3.10+ only."""
import functools
import http.server
import pathlib
import tempfile
import threading
import webbrowser
import zipfile
import sys

def main():
    # The archive contains only our trusted build output. No user archive is loaded.
    with tempfile.TemporaryDirectory(prefix="owon-ng-") as tmp:
        with zipfile.ZipFile(sys.argv[0]) as app:
            for entry in app.infolist():
                if entry.filename.startswith("web/"):
                    app.extract(entry, tmp)
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(pathlib.Path(tmp) / "web"))
        with http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
            url = f"http://127.0.0.1:{server.server_port}/"
            print(f"Owon NG — DEMO — {url}", flush=True)
            threading.Timer(0.5, webbrowser.open, args=(url,)).start()
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass

if __name__ == "__main__":
    main()
