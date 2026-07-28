import sys
from PIL import Image, ImageEnhance
import html

IMAGE_PATH = r"C:\Users\choya\OneDrive\Desktop\IMG_20260415_112529591_PORTRAIT2-892kb.jpg"
DARK_OUTPUT_PATH = r"C:\Users\choya\khushal-jangid\dark.svg"
LIGHT_OUTPUT_PATH = r"C:\Users\choya\khushal-jangid\light.svg"

# ASCII Charset for detailed portrait rendering
ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(img_path, width=54):
    try:
        img = Image.open(img_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)
        
    # Full image (No Cropping) so full portrait & body is shown
    w, h = img.size
    aspect_ratio = h / w
    height = int(width * aspect_ratio * 0.46)
    height = min(height, 56) # Fits comfortably inside 525px panel
    
    img = img.resize((width, height))
    img = img.convert("L")
    
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.85)
    
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
    laser_color = "#00F5D4" if is_dark else "#0284C7"
    
    # ASCII Art tspan generation (FULL PORTRAIT)
    tspan_lines = []
    start_y = 102
    line_spacing = 8.3
    for idx, line in enumerate(ascii_lines):
        y_pos = start_y + (idx * line_spacing)
        escaped_line = html.escape(line).replace(" ", "&#160;")
        tspan_lines.append(f'<tspan x="40" y="{y_pos:.1f}">{escaped_line}</tspan>')
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

  <linearGradient id="scanBeamGrad" x1="0%" y1="0%" x2="0%" y2="100%">
    <stop offset="0%" stop-color="{laser_color}" stop-opacity="0"/>
    <stop offset="70%" stop-color="{laser_color}" stop-opacity="0.35"/>
    <stop offset="100%" stop-color="{laser_color}" stop-opacity="0.95"/>
  </linearGradient>

  <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#7DD3FC" opacity="0.04"/>
  </pattern>

  <filter id="glowFilter" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="2.5" result="blur"/>
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
  
  .ascii-art {{ font-family: 'Courier New', monospace; font-size: 6.8px; fill: url(#asciiGrad); letter-spacing: 0.4px; }}
  
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

<!-- Left Panel: VISUAL.MAP (FULL UNCROPPED PORTRAIT) -->
<rect x="25" y="60" width="460" height="525" class="panel-box" />
<text x="45" y="82" class="panel-title">V I S U A L . M A P</text>

<text class="ascii-art">
{ascii_tspans}
</text>

<!-- Top-to-Bottom Moving Laser Beam Scanning Line (Left Panel Image Scan) -->
<rect x="30" y="90" width="450" height="18" fill="url(#scanBeamGrad)" opacity="0.6">
  <animate attributeName="y" from="90" to="560" dur="2.6s" repeatCount="indefinite" />
</rect>
<line x1="30" y1="108" x2="480" y2="108" stroke="{laser_color}" stroke-width="2.5" opacity="0.95" filter="url(#glowFilter)">
  <animate attributeName="y1" from="108" to="578" dur="2.6s" repeatCount="indefinite" />
  <animate attributeName="y2" from="108" to="578" dur="2.6s" repeatCount="indefinite" />
</line>

<!-- Global Terminal Vertical Scanning Beam (Top to Bottom across entire terminal) -->
<line x1="25" y1="60" x2="1155" y2="60" stroke="#38BDF8" stroke-width="1.5" opacity="0.7" filter="url(#glowFilter)">
  <animate attributeName="y1" from="60" to="580" dur="4s" repeatCount="indefinite" />
  <animate attributeName="y2" from="60" to="580" dur="4s" repeatCount="indefinite" />
</line>

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
        
    print("Successfully generated full uncropped portrait dark.svg & light.svg with top-to-bottom laser scan animation!")
