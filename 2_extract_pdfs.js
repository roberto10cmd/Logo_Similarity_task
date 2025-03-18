const puppeteer = require('puppeteer');
const fs = require('fs');
const readline = require('readline');

async function processURLs(filePath) {
    const browser = await puppeteer.launch();

    const fileStream = fs.createReadStream(filePath);
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    for await (const domain of rl) {
        const url = `https://${domain.trim()}`;
        if (url) {
            try {
                const page = await browser.newPage();

                await page.setViewport({ width: 1280, height: 300 });

                // navigheaza la pagina respectiva
                await page.goto(url, { waitUntil: 'networkidle2', timeout: 10000 });

                // incercare de eliminare a bannerului de cookies
                try {
                    await page.waitForSelector('button', { timeout: 2000 }); // waiting 2 second
                    const buttons = await page.$$('button');

                    for (const button of buttons) {
                        const text = await page.evaluate(el => el.innerText, button);
                        if (text.toLowerCase().includes('accept')) {
                            await button.click();
                            console.log(" Cookie banner închis.");
                            await page.waitForTimeout(2000);
                            break;
                        }
                    }
                } catch (error) {
                    console.log(" Nu s-a gasit un banner de cookies.");
                }

                // Creează PDF
                const outputFilePath = `output_pdfs/${domain.replace(/\./g, '_')}.pdf`;
                await page.pdf({
                    path: outputFilePath,
                    format: 'A4',
                    printBackground: true
                });

                console.log(`pdf creat pentru ${url}`);
                await page.close();

            } catch (error) {
                console.error(`Eroare la crearea pdf-ului pentru ${url}: ${error.message}`);
            }
        }
    }

    await browser.close();
}

processURLs('urls.txt');
