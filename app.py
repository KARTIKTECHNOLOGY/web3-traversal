from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Directory structure (created at runtime):
# /tmp/ctf_files/
#   public/
#     readme.txt
#     about.txt
#     help.txt
#   secret/
#     flag.txt      <-- target
#     notes.txt

BASE_DIR = "/tmp/ctf_files/public"
SECRET_DIR = "/tmp/ctf_files/secret"
FLAG = "Flag_CT8{p@th_tr@v3rs@l_d0t_d0t_sl@sh_2026}"

def setup_files():
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(SECRET_DIR, exist_ok=True)

    with open(f"{BASE_DIR}/readme.txt", "w") as f:
        f.write("Welcome to the CyberTec8 File Server.\nThis is a public document.\n")

    with open(f"{BASE_DIR}/about.txt", "w") as f:
        f.write("CyberTec8 is a cybersecurity training platform.\nVersion: 2.1.0\n")

    with open(f"{BASE_DIR}/help.txt", "w") as f:
        f.write("Use ?file=readme.txt to read files.\nOnly .txt files in the public folder are allowed... supposedly.\n")

    with open(f"{SECRET_DIR}/flag.txt", "w") as f:
        f.write(f"{FLAG}\n")

    with open(f"{SECRET_DIR}/notes.txt", "w") as f:
        f.write("Internal notes - keep confidential.\nAdmin password reset scheduled for Monday.\n")

PAGE = """
<!doctype html>
<html>
<head>
  <title>CyberTec8 File Server</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0f1117; color: #e2e8f0; font-family: 'Segoe UI', sans-serif; }
    .header { background: #1a1d27; padding: 16px 32px; border-bottom: 1px solid #2d3748; }
    .header h1 { color: #63b3ed; font-size: 1.1em; }
    .container { max-width: 750px; margin: 50px auto; padding: 0 20px; }
    .url-bar { display: flex; gap: 10px; margin-bottom: 28px; }
    .url-bar input { flex: 1; padding: 10px 14px; background: #1a1d27; border: 1px solid #2d3748; border-radius: 8px; color: #e2e8f0; font-family: monospace; font-size: 0.9em; }
    .url-bar button { padding: 10px 20px; background: #2b6cb0; border: none; border-radius: 8px; color: white; cursor: pointer; }
    .file-list { background: #1a1d27; border-radius: 10px; padding: 20px 24px; border: 1px solid #2d3748; margin-bottom: 20px; }
    .file-list h3 { color: #a0aec0; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 14px; }
    .file-link { display: block; padding: 8px 12px; color: #63b3ed; text-decoration: none; border-radius: 6px; font-family: monospace; font-size: 0.9em; }
    .file-link:hover { background: #2d3748; }
    .content-box { background: #1a1d27; border-radius: 10px; padding: 24px; border: 1px solid #2d3748; }
    .content-box h3 { color: #a0aec0; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 14px; }
    .file-content { font-family: monospace; font-size: 0.9em; white-space: pre-wrap; color: #e2e8f0; line-height: 1.6; }
    .error { color: #fc8181; font-style: italic; }
    .hint-box { margin-top: 20px; background: #1a202c; border-left: 3px solid #d69e2e; padding: 14px 18px; border-radius: 0 8px 8px 0; font-size: 0.83em; color: #d69e2e; }
    .breadcrumb { font-family: monospace; font-size: 0.82em; color: #4a5568; margin-bottom: 16px; }
  </style>
</head>
<body>
  <div class="header">
    <h1>📁 CyberTec8 File Server — Public Documents</h1>
  </div>
  <div class="container">

    <div class="url-bar">
      <form method="get" style="display:flex;width:100%;gap:10px">
        <input name="file" placeholder="filename (e.g. readme.txt)" value="{{ current_file }}">
        <button type="submit">Read File</button>
      </form>
    </div>

    <div class="breadcrumb">📂 /public/{{ current_file or '' }}</div>

    <div class="file-list">
      <h3>Public Files</h3>
      <a class="file-link" href="?file=readme.txt">📄 readme.txt</a>
      <a class="file-link" href="?file=about.txt">📄 about.txt</a>
      <a class="file-link" href="?file=help.txt">📄 help.txt</a>
    </div>

    {% if content %}
    <div class="content-box">
      <h3>📄 {{ current_file }}</h3>
      <div class="file-content {% if error %}error{% endif %}">{{ content }}</div>
    </div>
    {% endif %}

    <div class="hint-box">
      💡 <b>Hint:</b> The server reads files from a <code>public/</code> folder.
      What if you asked it to go <i>up</i> a directory?
    </div>

  </div>
</body>
</html>
"""

@app.route("/")
def index():
    filename = request.args.get("file", "")
    content = None
    error = False

    if filename:
        # VULNERABLE: no path sanitization — direct join with user input
        filepath = os.path.join(BASE_DIR, filename)
        try:
            with open(filepath, "r") as f:
                content = f.read()
        except FileNotFoundError:
            content = f"File not found: {filename}"
            error = True
        except PermissionError:
            content = f"Permission denied: {filename}"
            error = True
        except Exception as e:
            content = f"Error: {str(e)}"
            error = True

    return render_template_string(
        PAGE,
        current_file=filename,
        content=content,
        error=error
    )

if __name__ == "__main__":
    setup_files()
    print("="*60)
    print("Challenge running on port 7003")
    print(f"Flag is at: {SECRET_DIR}/flag.txt")
    print("Player must use: ?file=../secret/flag.txt")
    print("="*60)
    app.run(host="0.0.0.0", port=7003, debug=False)
