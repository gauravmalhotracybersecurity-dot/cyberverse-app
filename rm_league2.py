import re, glob, os

files = [f for f in glob.glob("**/app.html", recursive=True)
         if not any(x in f for x in ("venv", "node_modules", ".git"))]

js = """
<script id="disable-league">
(function(){
  function kill(){
    // 1. Hide any nav item whose label is "League"
    document.querySelectorAll('button, a, li').forEach(function(el){
      var t = (el.textContent || '').trim();
      if (/League$/i.test(t) && t.length <= 12) el.style.display = 'none';
    });
    // 2. Hide the Weekly League view (heading + its container)
    document.querySelectorAll('h1,h2,h3').forEach(function(h){
      if (/Weekly League/i.test(h.textContent)) {
        var sec = h.closest('section') || h.closest('div[id]') || h.parentElement;
        sec.style.display = 'none';
      }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', kill); else kill();
  setInterval(kill, 1200);
})();
</script>
"""

for f in files:
    s = open(f, encoding='utf-8').read()
    changed = False
    # clean previous attempts
    s2 = re.sub(r'<style id="disable-league">.*?</style>', '', s, flags=re.S)
    if s2 != s: s, changed = s2, True
    # static removal: nav button/link whose tag mentions league
    s2 = re.sub(r'<button(?=[^>]*league)[^>]*>.*?</button>', '', s, flags=re.S|re.I)
    if s2 != s: print('[REMOVED] static league button in', f); s, changed = s2, True
    s2 = re.sub(r'<a(?=[^>]*league)[^>]*>.*?</a>', '', s, flags=re.S|re.I)
    if s2 != s: print('[REMOVED] static league link in', f); s, changed = s2, True
    # inject runtime kill-switch
    if 'disable-league' not in s:
        s = s.replace('</body>', js + '\n</body>')
        changed = True
        print('[INJECTED] league kill-switch in', f)
    if changed:
        open(f, 'w', encoding='utf-8').write(s)

os.system('git add -A')
os.system('git commit -m "UI: fully remove League nav and view"')
os.system('git push origin main')
print('Pushed. Live in ~60s.')
