// Owon NG offline UI launcher. No USB or device access.
package main

import (
 "embed"
 "fmt"
 "io/fs"
 "log"
 "net"
 "net/http"
 "os"
 "os/exec"
 "runtime"
)
//go:embed web/*
var content embed.FS
var version = "development"
func main() {
 files, err := fs.Sub(content, "web"); if err != nil { log.Fatal(err) }
 listener, err := net.Listen("tcp", "127.0.0.1:0"); if err != nil { log.Fatal(err) }
 url := "http://" + listener.Addr().String() + "/"
 fmt.Printf("Owon NG %s — DEMO — %s\nSluit dit venster om te stoppen.\n", version, url)
 if os.Getenv("OWON_NO_BROWSER") != "1" {
  var command *exec.Cmd
  switch runtime.GOOS { case "windows": command = exec.Command("rundll32", "url.dll,FileProtocolHandler", url)
  case "darwin": command = exec.Command("open", url)
  default: command = exec.Command("xdg-open", url) }
  if err := command.Start(); err != nil { fmt.Println("Open handmatig:", url) }
 }
 log.Fatal(http.Serve(listener, http.FileServer(http.FS(files))))
}
