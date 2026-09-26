const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'], protocolTimeout: 0});
  const page = await browser.newPage();
  await page.goto('file://' + process.argv[2], {waitUntil: 'load', timeout: 0});
  await page.pdf({path: process.argv[3], format: 'A4', printBackground: true, timeout: 0,
    displayHeaderFooter: true, headerTemplate: '<div></div>',
    footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;font-family:DejaVu Sans">Диференциална диагноза · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: {top: '18mm', bottom: '18mm', left: '16mm', right: '16mm'}, outline: true, tagged: true});
  await browser.close();
})();
