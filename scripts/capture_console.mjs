import { chromium } from 'playwright';

const TARGET_URL = process.env.TARGET_URL || 'https://whatismydelta.com/';
const ASK_SELECTOR = '#coachAsk';

const log = (label, payload) => {
  const ts = new Date().toISOString();
  const data = typeof payload === 'string' ? payload : JSON.stringify(payload);
  console.log(`[${ts}] ${label} ${data}`);
};

(async () => {
  log('INFO', `Launching Chromium to capture console output from ${TARGET_URL}`);
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  page.on('console', (message) => {
    try {
      log(`BROWSER:${message.type().toUpperCase()}`, message.text());
    } catch (error) {
      log('ERROR', `Failed to serialize console message: ${error.message}`);
    }
  });

  page.on('pageerror', (error) => {
    log('BROWSER:PAGEERROR', error.toString());
  });

  page.on('requestfailed', (request) => {
    const failure = request.failure();
    log('BROWSER:REQUESTFAILED', {
      url: request.url(),
      method: request.method(),
      errorText: failure?.errorText || 'unknown error',
    });
  });

  try {
    await page.goto(TARGET_URL, { waitUntil: 'networkidle' });
    log('INFO', 'Page loaded, waiting for UI to settle');
    await page.waitForTimeout(2000);

    const hasAsk = await page.$(ASK_SELECTOR);
    if (!hasAsk) {
      log('WARN', `Selector ${ASK_SELECTOR} not found on page`);
    } else {
      log('INFO', 'Typing sample question into ask field');
      await page.fill(ASK_SELECTOR, 'What should I do next in my career?');
      await page.keyboard.press('Enter');
      log('INFO', 'Enter key pressed, waiting for potential responses');
      await page.waitForTimeout(6000);
    }
  } catch (error) {
    log('ERROR', `Script failed: ${error.message}`);
  } finally {
    await browser.close();
    log('INFO', 'Chromium session closed');
  }
})();
