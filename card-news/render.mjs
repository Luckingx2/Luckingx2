import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.join(__dirname, 'cards');
import { mkdirSync } from 'fs';
mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 2 });
await page.setViewportSize({ width: 1080, height: 1080 });
await page.goto('file://' + path.join(__dirname, 'index.html'));
await page.waitForTimeout(1200); // fonts

const cards = await page.$$('.card');
console.log('found', cards.length, 'cards');
let i = 1;
for (const c of cards) {
  const name = String(i).padStart(2, '0');
  await c.screenshot({ path: path.join(outDir, `card-${name}.png`) });
  console.log('saved card-' + name + '.png');
  i++;
}
await browser.close();
console.log('DONE');
