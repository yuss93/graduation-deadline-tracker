from datetime import date, datetime
from playwright.sync_api import sync_playwright
import os

TARGET_DATE = date(2027, 5, 22)
TODAY = date.today()
DAYS_LEFT = max((TARGET_DATE - TODAY).days, 0)

MILESTONES = [
    (90, "FINALIZE POST-GRAD PLANS", "May 2027"),
    (60, "SECURE CAP & GOWN", "March 2027"),
    (45, "SUBMIT DEGREE APPLICATION", "April 2027"),
    (30, "COMPLETE FINAL THESIS DRAFT", "April 2027"),
    (14, "FINAL PROJECT SUBMISSION", "May 2027"),
    (0,  "CCNY GRADUATION CEREMONY", "May 22, 2027"),
]

def build_html():
    milestone_cards = ""
    for t_minus, title, est_date in MILESTONES:
        completed = DAYS_LEFT < t_minus
        status_class = "completed" if completed else "active"
        badge_text = "DONE" if completed else f"T-{t_minus}D"
        milestone_cards += f"""
        <div class="card {status_class}">
            <div class="status-ring"></div>
            <div class="card-content">
                <div class="card-title">{title}</div>
                <div class="card-sub">Target Window: {est_date}</div>
            </div>
            <div class="badge">{badge_text}</div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CCNY Graduation Countdown HUD</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1170px;
    height: 2532px;
    background: radial-gradient(circle at 50% 25%, #162238 0%, #090d16 65%, #05070c 100%);
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", sans-serif;
    color: #f8fafc;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 640px 80px 180px 80px; /* Top padding leaves room for iOS/Android lock clock */
    position: relative;
    overflow: hidden;
  }}

  /* Subtle cyber grid background */
  body::before {{
    content: "";
    position: absolute;
    inset: 0;
    background-image: 
      linear-gradient(to right, rgba(56, 189, 248, 0.06) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(56, 189, 248, 0.06) 1px, transparent 1px);
    background-size: 90px 90px;
    z-index: 0;
  }}

  .container {{
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    gap: 36px;
  }}

  .header {{
    border-left: 8px solid #38bdf8;
    padding-left: 32px;
    margin-bottom: 12px;
  }}

  .header h1 {{
    font-size: 52px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #38bdf8;
    text-shadow: 0 0 24px rgba(56, 189, 248, 0.45);
  }}

  .header p {{
    font-size: 32px;
    color: #94a3b8;
    margin-top: 10px;
    font-weight: 500;
    letter-spacing: 1px;
  }}

  .milestones {{
    display: flex;
    flex-direction: column;
    gap: 28px;
  }}

  .card {{
    background: rgba(15, 23, 42, 0.78);
    border: 2px solid rgba(56, 189, 248, 0.35);
    border-radius: 28px;
    padding: 36px 42px;
    display: flex;
    align-items: center;
    gap: 32px;
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.08);
  }}

  .card.completed {{
    border-color: rgba(34, 197, 94, 0.45);
    opacity: 0.72;
  }}

  .status-ring {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: 5px solid #38bdf8;
    box-shadow: 0 0 16px rgba(56, 189, 248, 0.6);
    flex-shrink: 0;
  }}

  .card.completed .status-ring {{
    border-color: #22c55e;
    background: #22c55e;
    box-shadow: 0 0 16px rgba(34, 197, 94, 0.6);
  }}

  .card-content {{
    flex: 1;
  }}

  .card-title {{
    font-size: 36px;
    font-weight: 700;
    letter-spacing: 0.8px;
    color: #f1f5f9;
  }}

  .card-sub {{
    font-size: 26px;
    color: #94a3b8;
    margin-top: 6px;
  }}

  .badge {{
    background: rgba(56, 189, 248, 0.15);
    border: 2px solid #38bdf8;
    color: #38bdf8;
    font-size: 28px;
    font-weight: 700;
    padding: 12px 24px;
    border-radius: 16px;
    letter-spacing: 1px;
  }}

  .countdown-box {{
    position: relative;
    z-index: 1;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(30, 41, 59, 0.88));
    border: 3px solid #38bdf8;
    border-radius: 36px;
    padding: 48px;
    text-align: center;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.8), 0 0 35px rgba(56, 189, 248, 0.28);
  }}

  .countdown-number {{
    font-size: 86px;
    font-weight: 800;
    color: #38bdf8;
    letter-spacing: 3px;
    text-shadow: 0 0 30px rgba(56, 189, 248, 0.5);
  }}

  .countdown-target {{
    font-size: 32px;
    color: #cbd5e1;
    margin-top: 14px;
    letter-spacing: 2px;
    font-weight: 600;
  }}
</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>T-MINUS: GRADUATION</h1>
      <p>CCNY B.E. COMPUTER ENGINEERING • CLASS OF 2027</p>
    </div>
    <div class="milestones">
      {milestone_cards}
    </div>
  </div>

  <div class="countdown-box">
    <div class="countdown-number" id="timer">T - {DAYS_LEFT:03d} DAYS</div>
    <div class="countdown-target">TARGET: MAY 22, 2027</div>
  </div>

  <script>
    // Live second-by-second ticker when viewed in a browser
    const target = new Date("2027-05-22T09:00:00").getTime();
    function updateClock() {{
      const now = Date.now();
      const diff = Math.max(target - now, 0);
      const d = Math.floor(diff / (1000 * 60 * 60 * 24));
      const h = Math.floor((diff / (1000 * 60 * 60)) % 24);
      const m = Math.floor((diff / 1000 / 60) % 60);
      const s = Math.floor((diff / 1000) % 60);
      document.getElementById("timer").textContent = 
        `${{String(d).padStart(3, '0')}}D : ${{String(h).padStart(2, '0')}}H : ${{String(m).padStart(2, '0')}}M : ${{String(s).padStart(2, '0')}}S`;
    }}
    updateClock();
    setInterval(updateClock, 1000);
  </script>
</body>
</html>
"""
    with open("index.html", "w") as f:
        f.write(html_content)

def render_png(output_path="graduation_lockscreen.png"):
    build_html()
    html_uri = "file://" + os.path.abspath("index.html")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1170, "height": 2532})
        page.goto(html_uri)
        page.wait_for_timeout(300)
        page.screenshot(path=output_path)
        browser.close()
    print(f"Rendered high-res UI lock screen to {output_path} and live web HUD to index.html")

if __name__ == "__main__":
    render_png()
