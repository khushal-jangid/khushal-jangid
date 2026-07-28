import sys
from PIL import Image, ImageEnhance
import html

IMAGE_PATH = r"C:\Users\choya\OneDrive\Desktop\IMG_20260415_112529591_PORTRAIT2-892kb.jpg"
DARK_OUTPUT_PATH = r"C:\Users\choya\khushal-jangid\dark.svg"
LIGHT_OUTPUT_PATH = r"C:\Users\choya\khushal-jangid\light.svg"

# ASCII Charset for rendering contrast
ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(img_path, width=64):
    try:
        img = Image.open(img_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)
        
    # Crop to upper torso / face (top 75% of the portrait)
    w, h = img.size
    img = img.crop((0, 0, w, int(h * 0.75)))
    
    # Calculate aspect ratio
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.45)
    height = min(height, 58) # max lines fit in panel
    
    img = img.resize((width, height))
    img = img.convert("L") # convert to grayscale
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.8)
    
    pixels = img.getdata()
    ascii_str = ""
    for pixel in pixels:
        index = int((pixel / 255) * (len(ASCII_CHARS) - 1))
        ascii_str += ASCII_CHARS[index]
        
    ascii_lines = []
    for i in range(0, len(ascii_str), width):
        ascii_lines.append(ascii_str[i:i+width])
        
    return ascii_lines

def build_svg(ascii_lines, theme="dark"):
    is_dark = (theme == "dark")
    
    bg_color = "#0B1120" if is_dark else "#F8FAFC"
    border_start = "#7C3AED" if is_dark else "#3B82F6"
    border_mid = "#22D3EE" if is_dark else "#06B6D4"
    border_end = "#10B981" if is_dark else "#10B981"
    
    panel_bg = "#0F172A" if is_dark else "#FFFFFF"
    panel_stroke = "#1E293B" if is_dark else "#E2E8F0"
    
    text_hdr = "#38BDF8" if is_dark else "#0284C7"
    text_key = "#38BDF8" if is_dark else "#0369A1"
    text_val = "#E2E8F0" if is_dark else "#0F172A"
    text_dim = "#64748B" if is_dark else "#94A3B8"
    text_sec = "#10B981" if is_dark else "#059669"
    
    # ASCII Art tspan generation
    tspan_lines = []
    start_y = 100
    line_spacing = 8.2
    for idx, line in enumerate(ascii_lines):
        y_pos = start_y + (idx * line_spacing)
        escaped_line = html.escape(line).replace(" ", "&#160;")
        tspan_lines.append(f'<tspan x="45" y="{y_pos:.1f}">{escaped_line}</tspan>')
    ascii_tspans = "\n".join(tspan_lines)
    
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610">
<defs>
  <linearGradient id="asciiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#22D3EE">
      <animate attributeName="stop-color" values="#22D3EE;#7C3AED;#38BDF8;#22D3EE" dur="9s" repeatCount="indefinite"/>
    </stop>
    <stop offset="100%" stop-color="#7C3AED">
      <animate attributeName="stop-color" values="#7C3AED;#38BDF8;#22D3EE;#7C3AED" dur="9s" repeatCount="indefinite"/>
    </stop>
  </linearGradient>
  <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="{border_start}"/>
    <stop offset="50%" stop-color="{border_mid}"/>
    <stop offset="100%" stop-color="{border_end}"/>
  </linearGradient>
  <linearGradient id="laserBeamGrad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#22D3EE" stop-opacity="0"/>
    <stop offset="20%" stop-color="#22D3EE" stop-opacity="0.8"/>
    <stop offset="50%" stop-color="#A5F3FC" stop-opacity="1"/>
    <stop offset="80%" stop-color="#7C3AED" stop-opacity="0.8"/>
    <stop offset="100%" stop-color="#7C3AED" stop-opacity="0"/>
  </linearGradient>
  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#7DD3FC" opacity="0.04"/>
  </pattern>
  <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="3" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
  <mask id="revealMask" maskUnits="userSpaceOnUse" x="0" y="0" width="1180" height="620">
    <rect x="0" y="0" width="1180" height="0" fill="#fff">
      <animate attributeName="height" from="0" to="610" dur="2.2s" begin="0.1s" fill="freeze" calcMode="spline" keySplines="0.25 0.1 0.25 1"/>
    </rect>
  </mask>
</defs>

<style>
  .term-bg {{ fill: {bg_color}; }}
  .window-border {{ fill: none; stroke: url(#borderGrad); stroke-width: 2; rx: 12; }}
  .dot-red {{ fill: #EF4444; }}
  .dot-yellow {{ fill: #F59E0B; }}
  .dot-green {{ fill: #10B981; }}
  .title-text {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 13px; fill: {text_dim}; }}
  .header-live {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 11px; fill: #EF4444; font-weight: bold; }}
  
  .panel-box {{ fill: {panel_bg}; fill-opacity: 0.75; stroke: {panel_stroke}; stroke-width: 1; rx: 8; }}
  .panel-title {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 11px; letter-spacing: 2px; fill: {text_dim}; font-weight: bold; }}
  
  .ascii-art {{ font-family: 'Courier New', monospace; font-size: 7.2px; fill: url(#asciiGrad); letter-spacing: 0.5px; }}
  
  .user-header {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 15px; font-weight: bold; fill: {text_hdr}; }}
  .label-key {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 12.5px; font-weight: bold; fill: {text_key}; }}
  .label-val {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 12.5px; fill: {text_val}; }}
  .label-dim {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 12.5px; fill: {text_dim}; }}
  .section-hdr {{ font-family: 'Fira Code', 'Courier New', monospace; font-size: 12.5px; font-weight: bold; fill: {text_sec}; }}
</style>

<!-- Main Container -->
<rect width="1180" height="610" rx="12" class="term-bg" />
<rect width="1178" height="608" x="1" y="1" rx="12" class="window-border" />
<rect width="1180" height="610" fill="url(#scanlines)" />

<!-- Window Controls -->
<circle cx="45" cy="30" r="6" class="dot-red" />
<circle cx="65" cy="30" r="6" class="dot-yellow" />
<circle cx="85" cy="30" r="6" class="dot-green" />

<!-- Top Window Bar -->
<text x="590" y="34" text-anchor="middle" class="title-text">khushal@devos ~ % ./profile.sh --live</text>
<text x="1110" y="34" text-anchor="end" class="header-live">
  <tspan fill="#EF4444">🔴 SCANNING</tspan>
  <animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite" />
</text>

<!-- Left Panel: VISUAL.MAP -->
<rect x="25" y="60" width="460" height="525" class="panel-box" />
<text x="45" y="82" class="panel-title">V I S U A L . M A P</text>

<text class="ascii-art">
{ascii_tspans}
</text>

<!-- Right Panel: SYSTEM.INFO -->
<rect x="500" y="60" width="655" height="525" class="panel-box" />
<text x="520" y="82" class="panel-title">S Y S T E M . I N F O</text>

<!-- Animated Right Panel Content -->
<g mask="url(#revealMask)">
  <text x="520" y="115" class="user-header">khushal@devos -------------------------------------------</text>
  
  <text x="520" y="142"><tspan class="label-key">. Subject:</tspan><tspan class="label-dim"> ................................. </tspan><tspan class="label-val">Khushal Jangid</tspan></text>
  <text x="520" y="166"><tspan class="label-key">. Role:</tspan><tspan class="label-dim"> .................................... </tspan><tspan class="label-val">B.Tech CSE Student · Aspiring DevOps &amp; Cloud Engineer</tspan></text>
  <text x="520" y="190"><tspan class="label-key">. Origin:</tspan><tspan class="label-dim"> .................................. </tspan><tspan class="label-val">India</tspan></text>
  <text x="520" y="214"><tspan class="label-key">. Education:</tspan><tspan class="label-dim"> ............................... </tspan><tspan class="label-val">B.Tech Computer Science &amp; Engineering</tspan></text>
  <text x="520" y="238"><tspan class="label-key">. Status:</tspan><tspan class="label-dim"> .................................. </tspan><tspan class="label-val">Building · Learning · Automating</tspan></text>
  <text x="520" y="262"><tspan class="label-key">. ToolChain:</tspan><tspan class="label-dim"> ................................ </tspan><tspan class="label-val">Docker, Kubernetes, Terraform, Ansible, AWS, GCP</tspan></text>

  <text x="520" y="295"><tspan class="label-key">. Core.Cloud:</tspan><tspan class="label-dim"> ............................... </tspan><tspan class="label-val">AWS, Google Cloud, Azure (learning)</tspan></text>
  <text x="520" y="319"><tspan class="label-key">. Core.DevOps:</tspan><tspan class="label-dim"> .............................. </tspan><tspan class="label-val">Docker, Kubernetes, Jenkins, Actions, Terraform, Ansible</tspan></text>
  <text x="520" y="343"><tspan class="label-key">. Core.System:</tspan><tspan class="label-dim"> .............................. </tspan><tspan class="label-val">Linux, Bash Scripting, Networking, Git &amp; GitHub</tspan></text>
  <text x="520" y="367"><tspan class="label-key">. Core.Lang:</tspan><tspan class="label-dim"> ................................ </tspan><tspan class="label-val">Python, Java, JavaScript, HTML, CSS</tspan></text>
  <text x="520" y="391"><tspan class="label-key">. Core.Projects:</tspan><tspan class="label-dim"> ............................ </tspan><tspan class="label-val">Smart Secure File Sharing, Codeware, Cloud AI</tspan></text>

  <text x="520" y="425" class="section-hdr">- Contact ----------------------------------------------------</text>
  <text x="520" y="449"><tspan class="label-key">. Grid.Mail:</tspan><tspan class="label-dim"> ................................ </tspan><tspan class="label-val">khushal.jangid.devops@gmail.com</tspan></text>
  <text x="520" y="473"><tspan class="label-key">. Grid.LinkedIn:</tspan><tspan class="label-dim"> ............................ </tspan><tspan class="label-val">khushal-jangid</tspan></text>
  <text x="520" y="497"><tspan class="label-key">. Grid.Github:</tspan><tspan class="label-dim"> .............................. </tspan><tspan class="label-val">khushal-jangid</tspan></text>

  <text x="520" y="530" class="section-hdr">- Live Stats --------------------------------------------------</text>
  <text x="520" y="554"><tspan class="label-val"> See live GitHub stats badges below in README ↓</tspan></text>
</g>

<!-- Moving Laser Beam Scanning Line Animation across the terminal window -->
<rect x="25" y="60" width="1130" height="3" fill="url(#laserBeamGrad)" filter="url(#softGlow)">
  <animate attributeName="y" values="60;575;60" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1; 0.4 0 0.6 1" />
</rect>

</svg>"""
    return svg_content

if __name__ == "__main__":
    ascii_art = image_to_ascii(IMAGE_PATH)
    dark_svg = build_svg(ascii_art, theme="dark")
    light_svg = build_svg(ascii_art, theme="light")
    
    with open(DARK_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(LIGHT_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(light_svg)
        
    print("Successfully generated dark.svg and light.svg with scanning animation!")
