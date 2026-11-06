package nl.owon.ng;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import java.io.ByteArrayInputStream;
import java.io.IOException;

public final class MainActivity extends Activity {
    private WebView view;
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        view = new WebView(this);
        setContentView(view);
        view.setBackgroundColor(0xff10171e);
        view.setWebChromeClient(new WebChromeClient());
        view.getSettings().setJavaScriptEnabled(true);
        view.getSettings().setUserAgentString(view.getSettings().getUserAgentString() + " OwonNGAndroid");
        view.getSettings().setDomStorageEnabled(true);
        // Content is served only from the packaged assets. No network permission.
        view.getSettings().setAllowFileAccess(false);
        view.getSettings().setAllowContentAccess(false);
        view.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView web, WebResourceRequest request) {
                return !request.getUrl().toString().startsWith("https://app.owon.invalid/");
            }
            @Override public WebResourceResponse shouldInterceptRequest(WebView web, WebResourceRequest request) {
                if (!"app.owon.invalid".equals(request.getUrl().getHost())) {
                    return new WebResourceResponse("text/plain", "UTF-8", new ByteArrayInputStream(new byte[0]));
                }
                String path = request.getUrl().getPath();
                if (path == null || path.equals("/")) path = "/index.html";
                if (path.contains("..")) return null;
                String mime = path.endsWith(".js") ? "application/javascript" : path.endsWith(".css") ? "text/css" : "text/html";
                try { return new WebResourceResponse(mime, "UTF-8", getAssets().open("web" + path)); }
                catch (IOException e) { return new WebResourceResponse("text/plain", "UTF-8", new ByteArrayInputStream("Asset unavailable".getBytes())); }
            }
        });
        view.loadUrl("https://app.owon.invalid/");
    }
    @Override protected void onDestroy() { view.destroy(); super.onDestroy(); }
}
