/**
 * CMP-3 FE Tests: Tu Vi Compatibility
 * TDD — written BEFORE implementation (red first).
 * 4 tests: form submit, score circle, factor bars, streaming analysis.
 */

HTMLElement.prototype.scrollTo = jest.fn();
HTMLElement.prototype.scrollIntoView = jest.fn();

// ── Full DOM ──
document.body.innerHTML = `
  <div id="cmp-section" class="hidden">
    <button id="btn-cmp-open"></button>
    <div id="cmp-panel" class="hidden">
      <!-- Person A inputs -->
      <input id="cmp-a-name" value="">
      <input id="cmp-a-year" type="number" value="1993">
      <input id="cmp-a-month" type="number" value="6">
      <input id="cmp-a-day" type="number" value="13">
      <select id="cmp-a-hour"><option value="10">10</option></select>
      <div class="cmp-gender-toggle">
        <button class="cmp-gender-btn active" data-person="a" data-gender="nam">Nam</button>
        <button class="cmp-gender-btn" data-person="a" data-gender="nu">Nữ</button>
      </div>
      <!-- Person B inputs -->
      <input id="cmp-b-name" value="">
      <input id="cmp-b-year" type="number" value="1995">
      <input id="cmp-b-month" type="number" value="3">
      <input id="cmp-b-day" type="number" value="22">
      <select id="cmp-b-hour"><option value="14">14</option></select>
      <div class="cmp-gender-toggle">
        <button class="cmp-gender-btn active" data-person="b" data-gender="nu">Nữ</button>
        <button class="cmp-gender-btn" data-person="b" data-gender="nam">Nam</button>
      </div>
      <!-- Submit -->
      <button id="cmp-submit-btn" onclick="submitCompatibility()">So sánh</button>
      <!-- Status -->
      <div id="cmp-loading" class="hidden"></div>
      <div id="cmp-error" class="hidden"></div>
      <!-- Results -->
      <div id="cmp-results" class="hidden">
        <!-- Score circle -->
        <div id="cmp-score-circle">
          <span id="cmp-score-value"></span>
          <span id="cmp-score-rating"></span>
        </div>
        <!-- Factor bars -->
        <div id="cmp-factors">
          <div class="cmp-factor-bar" id="cmp-factor-ngu-hanh">
            <div class="cmp-factor-fill"></div>
            <span class="cmp-factor-detail"></span>
          </div>
          <div class="cmp-factor-bar" id="cmp-factor-zodiac">
            <div class="cmp-factor-fill"></div>
            <span class="cmp-factor-detail"></span>
          </div>
          <div class="cmp-factor-bar" id="cmp-factor-phu-the">
            <div class="cmp-factor-fill"></div>
            <span class="cmp-factor-detail"></span>
          </div>
          <div class="cmp-factor-bar" id="cmp-factor-menh">
            <div class="cmp-factor-fill"></div>
            <span class="cmp-factor-detail"></span>
          </div>
        </div>
        <!-- Streaming analysis -->
        <div id="cmp-analysis-section">
          <div id="cmp-analysis-content"></div>
        </div>
      </div>
    </div>
  </div>
  <!-- Other TV elements needed by module load -->
  <div id="chart-container"></div>
  <div id="ai-section" class="hidden"></div>
  <div id="share-section" class="hidden"></div>
  <div id="ln-section" class="hidden"></div>
  <div id="ln-panel" class="hidden"></div>
`;

// ── Globals (must be before require) ──
global.renderMarkdown = jest.fn(t => `<p>${t}</p>`);
global.readSSEStream  = jest.fn(() => Promise.resolve());
global.getDeviceId    = jest.fn(() => 'test-device');
global.tuviApi        = { getChart: jest.fn() };
global.alert          = jest.fn();
global.fetch          = jest.fn(() => Promise.resolve({ ok: true, json: async () => ({}) }));
global.API_BASE       = '';
global.localStorage   = { getItem: jest.fn(() => null), setItem: jest.fn(), removeItem: jest.fn() };

jest.resetModules();
const mod = require('../js/tuvi-chart.js');
const {
    submitCompatibility,
    renderCompatibilityResult,
    streamCompatibilityAnalysis,
    selectCompatibilityGender,
    autoFillPersonAFromProfile,
} = mod;

// ── Mock API response ──
function mockCompatibilityData(score = 78) {
    return {
        score,
        rating: score >= 80 ? 'Rất hợp' : score >= 60 ? 'Khá hợp' : 'Bình thường',
        factors: {
            ngu_hanh:    { score: 25, detail: 'Kim sinh Thủy — Tương Sinh' },
            zodiac:      { score: 22, detail: 'Dậu-Hợi — Lục Hợp' },
            phu_the:     { score: 18, detail: 'A: Thái Âm (miếu), B: Tham Lang' },
            menh_harmony:{ score: 13, detail: 'Tý-Thân — Tam Hợp' },
        },
        person_a: { name: 'Anh', menh: 'Mệnh', cuc: 'Kim Tứ Cục', zodiac: 'Dậu' },
        person_b: { name: 'Em',  menh: 'Mệnh', cuc: 'Thủy Nhị Cục', zodiac: 'Hợi' },
    };
}

beforeEach(() => {
    jest.clearAllMocks();
    document.getElementById('cmp-results').classList.add('hidden');
    document.getElementById('cmp-loading').classList.add('hidden');
    document.getElementById('cmp-error').classList.add('hidden');
    document.getElementById('cmp-score-value').textContent = '';
    document.getElementById('cmp-score-rating').textContent = '';
    document.getElementById('cmp-analysis-content').innerHTML = '';
    // Reset factor fills
    document.querySelectorAll('.cmp-factor-fill').forEach(f => { f.style.width = ''; });
    document.querySelectorAll('.cmp-factor-detail').forEach(f => { f.textContent = ''; });
});

// ════════════════════════════════════════════════════════
// Test 1: Two-person form submits correct POST body
// ════════════════════════════════════════════════════════
test('submitCompatibility sends correct POST body with both persons data', async () => {
    document.getElementById('cmp-a-name').value = 'Anh';
    document.getElementById('cmp-a-year').value = '1993';
    document.getElementById('cmp-a-month').value = '6';
    document.getElementById('cmp-a-day').value = '13';
    document.getElementById('cmp-b-name').value = 'Em';
    document.getElementById('cmp-b-year').value = '1995';
    document.getElementById('cmp-b-month').value = '3';
    document.getElementById('cmp-b-day').value = '22';

    const mockData = mockCompatibilityData();
    global.fetch = jest.fn(() => Promise.resolve({
        ok: true,
        json: async () => mockData,
        body: {},
    }));

    await submitCompatibility();

    expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/tuvi/compatibility'),
        expect.objectContaining({ method: 'POST' })
    );

    const callArgs = global.fetch.mock.calls[0];
    const body = JSON.parse(callArgs[1].body);
    expect(body.person_a.name).toBe('Anh');
    expect(body.person_a.year).toBe(1993);
    expect(body.person_b.name).toBe('Em');
    expect(body.person_b.year).toBe(1995);
    expect(body.device_id).toBe('test-device');
});

// ════════════════════════════════════════════════════════
// Test 2: Score circle renders value + rating + color class
// ════════════════════════════════════════════════════════
test('renderCompatibilityResult renders score circle with value and rating', () => {
    renderCompatibilityResult(mockCompatibilityData(78));

    const valueEl  = document.getElementById('cmp-score-value');
    const ratingEl = document.getElementById('cmp-score-rating');
    const circle   = document.getElementById('cmp-score-circle');

    expect(valueEl.textContent).toBe('78');
    expect(ratingEl.textContent).toBe('Khá hợp');

    // Color class — 60-79 = yellow/good range
    expect(
        circle.classList.contains('score-good') ||
        circle.classList.contains('score-medium') ||
        circle.classList.contains('score-khá')
    ).toBe(true);

    // Results panel becomes visible
    expect(document.getElementById('cmp-results').classList.contains('hidden')).toBe(false);
});

// ════════════════════════════════════════════════════════
// Test 3: 4 factor bars render with correct widths + details
// ════════════════════════════════════════════════════════
test('renderCompatibilityResult renders all 4 factor bars with details', () => {
    renderCompatibilityResult(mockCompatibilityData(78));

    const bars = document.querySelectorAll('.cmp-factor-bar');
    expect(bars.length).toBe(4);

    // Each bar should have a fill width set (% of 25pt max)
    const fills = document.querySelectorAll('.cmp-factor-fill');
    fills.forEach(fill => {
        expect(fill.style.width).toMatch(/%$/);
        expect(parseFloat(fill.style.width)).toBeGreaterThan(0);
    });

    // Detail text populated for each factor
    const details = document.querySelectorAll('.cmp-factor-detail');
    const detailTexts = Array.from(details).map(d => d.textContent);
    expect(detailTexts.some(t => t.includes('Tương Sinh'))).toBe(true);
    expect(detailTexts.some(t => t.includes('Lục Hợp'))).toBe(true);
});

// ════════════════════════════════════════════════════════
// Test 4: Streaming analysis calls readSSEStream + renders markdown
// ════════════════════════════════════════════════════════
test('streamCompatibilityAnalysis calls fetch SSE endpoint and renders markdown output', async () => {
    const streamData = mockCompatibilityData(78);

    global.readSSEStream = jest.fn(async (response, el) => {
        el.innerHTML = renderMarkdown('Hai người rất hợp nhau.');
        return Promise.resolve();
    });

    global.fetch = jest.fn(() => Promise.resolve({
        ok: true,
        body: {},
    }));

    await streamCompatibilityAnalysis(streamData);

    expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/tuvi/compatibility/stream'),
        expect.objectContaining({ method: 'POST' })
    );

    const content = document.getElementById('cmp-analysis-content');
    expect(content.innerHTML).toContain('hợp nhau');
});
