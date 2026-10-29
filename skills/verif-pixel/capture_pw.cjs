// node capture_pw.cjs <url> <out.png> [largeur=1440] [hauteur=900] [light|dark] [selecteur]
// Capture sans que le modele regarde l'image (a enchainer avec verif_pixel.py).
const path = require('path');
const root = process.env.PW_ROOT || process.cwd(); // dossier contenant node_modules/playwright-core
const { chromium } = require(path.join(root, 'node_modules', 'playwright-core'));
(async () => {
  const [url, out, w = '1440', h = '900', scheme = 'light', sel] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: process.env.CHROME || 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', headless: true });
  const ctx = await b.newContext({ viewport: { width: +w, height: +h }, colorScheme: scheme });
  const p = await ctx.newPage();
  await p.goto(url); await p.waitForTimeout(1500);
  if (sel) await p.locator(sel).first().screenshot({ path: out });
  else await p.screenshot({ path: out, fullPage: true });
  console.log('ok', out);
  await b.close();
})();
