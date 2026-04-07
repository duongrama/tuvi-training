/**
 * FRM-2: TV og:image path — must be /static/img/og-card.png
 * Tu Vi mounts frontend at /static, so og:image must include the prefix.
 */
const fs = require('fs');
const path = require('path');

const indexHtml = fs.readFileSync(
    path.join(__dirname, '../index.html'),
    'utf8'
);

test('og:image uses /static/img/og-card.png (TV serves at /static mount)', () => {
    expect(indexHtml).toContain('content="/static/img/og-card.png"');
});

test('og:image does NOT use bare /img/og-card.png (would 404 on TV)', () => {
    // Must not have the un-prefixed path as og:image value
    expect(indexHtml).not.toMatch(/property="og:image"\s+content="\/img\/og-card\.png"/);
});
