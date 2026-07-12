from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Voice Check</title>

<style>
body{
    font-family: Arial, sans-serif;
    background:#111827;
    color:white;
    padding:40px;
}

h1{
    color:#4ade80;
}

button{
    padding:12px 20px;
    font-size:18px;
    cursor:pointer;
    border:none;
    border-radius:8px;
    background:#2563eb;
    color:white;
}

#output{
    margin-top:30px;
    border:1px solid #444;
    padding:20px;
    min-height:250px;
    white-space:pre-wrap;
    font-size:22px;
    background:#1f2937;
}
</style>

</head>

<body>

<h1>🎤 Voice Recognition Test</h1>

<button id="start">Start Listening</button>

<div id="output"></div>

<script>
const output = document.getElementById("output");

const SpeechRecognition =
window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
    output.innerHTML = "Speech Recognition NOT supported.";
} else {

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = true;
    recognition.interimResults = true;

    let started = false;

    document.getElementById("start").onclick = () => {

        if (started) return;

        started = true;

        recognition.start();

    };

    recognition.onstart = () => {
        output.innerHTML = "🎤 Microphone started...<br><br>";
        console.log("STARTED");
    };

    recognition.onaudiostart = () => {
        console.log("AUDIO START");
        output.innerHTML += "Audio detected.<br>";
    };

    recognition.onsoundstart = () => {
        console.log("SOUND START");
        output.innerHTML += "Sound detected.<br>";
    };

    recognition.onspeechstart = () => {
        console.log("SPEECH START");
        output.innerHTML += "Speech detected.<br>";
    };

    recognition.onresult = (event) => {

        console.log(event);

        let transcript = "";

        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }

        output.innerHTML += "<br><b>" + transcript + "</b>";

    };

    recognition.onerror = (event) => {
        console.log(event);
        output.innerHTML += "<br>ERROR: " + event.error;
    };

    recognition.onend = () => {
        console.log("ENDED");
        started = false;
        recognition.start();
    };

}
</script>

</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML.encode())


server = HTTPServer(("localhost", 8080), Handler)

print("Opening browser...")

webbrowser.open("http://localhost:8080")

print("Server running at http://localhost:8080")

server.serve_forever()