/**
 * Sprint 65 Item 1 — TV P2-5: Star Brightness Display Enhancement
 * TDD — tests written BEFORE implementation (red first).
 * 2 tests: hover popup shows brightness_effect, brightness legend renders 5 entries.
 */

HTMLElement.prototype.scrollTo = jest.fn();
HTMLElement.prototype.scrollIntoView = jest.fn();

document.body.innerHTML = `
  <div id="chart-container"></div>
  <div id="ai-section" class="hidden"></div>
  <div id="share-section" class="hidden"></div>
  <div id="ln-section" class="hidden"></div>
  <div id="ln-panel" class="hidden"></div>
`;

global.renderMarkdown = jest.fn(t => t);
global.readSSEStream  = jest.fn(() => Promise.resolve());
global.getDeviceId    = jest.fn(() => 'test-device');
global.tuviApi        = { getChart: jest.fn() };
global.alert          = jest.fn();
global.fetch          = jest.fn(() => Promise.resolve({ ok: true, json: async () => ({}) }));
global.API_BASE       = '';
global.localStorage   = { getItem: jest.fn(() => null), setItem: jest.fn(), removeItem: jest.fn() };

jest.resetModules();
const mod = require('../js/tuvi-chart.js');
const { buildDetailHTML, buildCenterPanelHTML } = mod;

// ════════════════════════════════════════════════════════
// Test 1: Hover popup shows brightness_effect text
// ════════════════════════════════════════════════════════
test('buildDetailHTML shows brightness_effect text in star card when available', () => {
    const palace = {
        position: 1,
        cung_name: 'Mệnh',
        meaning: '',
        can_chi: 'Tý',
        stars: [
            {
                name: 'Tử Vi',
                brightness: 'Miếu',
                tu_hoa: null,
                element: 'Earth',
                brightness_effect: 'Ở thế cực vượng, phát huy tối đa năng lực lãnh đạo',
            }
        ],
        adjective_stars: [],
        dai_han: null,
    };

    const html = buildDetailHTML(palace);

    expect(html).toContain('star-brightness-effect');
    expect(html).toContain('Ở thế cực vượng');
});

// ════════════════════════════════════════════════════════
// Test 2: Brightness legend renders 5 entries
// ════════════════════════════════════════════════════════
test('buildCenterPanelHTML includes brightness legend with 5 entries', () => {
    const data = {
        birth: { solar: { day: 1, month: 1, year: 1993 }, lunar: { day: 1, month: 1, year: 1993 } },
        nap_am: { name: 'Kim' },
        cuc: { name: 'Kim Tứ Cục' },
        menh_chu: 'Vũ Khúc',
        than_chu: 'Thiên Tướng',
        tu_hoa: null,
        cung_menh: 'Tý',
        cung_than: 'Ngọ',
    };

    const html = buildCenterPanelHTML(data);

    // Legend should have all 5 brightness levels
    expect(html).toContain('Miếu');
    expect(html).toContain('Vượng');
    expect(html).toContain('Đắc');
    expect(html).toContain('Bình');
    expect(html).toContain('Hãm');
    // Should have a legend container
    expect(html).toContain('brightness-legend');
});
