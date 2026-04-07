/**
 * LN-3: Lưu Niên Yearly Forecast — FE Tests
 * 4 tests covering: year selector, 12-month grid, month click detail, rating colors
 */

HTMLElement.prototype.scrollTo = jest.fn();
HTMLElement.prototype.scrollIntoView = jest.fn();

// ── DOM Setup ──
document.body.innerHTML = `
  <div id="ln-section" class="hidden"></div>
  <div id="ln-panel" class="hidden">
    <button id="ln-year-prev"></button>
    <select id="ln-year-select"></select>
    <button id="ln-year-next"></button>
    <div id="ln-overview" class="hidden">
      <div id="ln-year-title"></div>
      <span id="ln-nominal-age"></span>
      <span id="ln-menh-palace"></span>
      <div id="ln-tuhoa"></div>
    </div>
    <div id="ln-loading" class="hidden">Đang tải...</div>
    <div id="ln-error" class="hidden"></div>
    <div id="ln-month-grid"></div>
    <div id="ln-month-detail" class="hidden">
      <span id="ln-detail-title"></span>
      <button class="ln-detail-close"></button>
      <div id="ln-detail-body"></div>
    </div>
  </div>
  <div id="chart-container"></div>
  <div id="ai-section" class="hidden"></div>
  <div id="share-section" class="hidden"></div>
`;

// ── Global mocks (must be before require) ──
global.renderMarkdown = jest.fn(t => t);
global.readSSEStream  = jest.fn(() => Promise.resolve());
global.getDeviceId    = jest.fn(() => 'test-device');
global.tuviApi        = { getChart: jest.fn() };
global.alert          = jest.fn();
global.fetch          = jest.fn(() => Promise.resolve({ ok: true, json: async () => ({}) }));

const {
    loadYearlyForecast,
    renderYearlyForecast,
    showLuuNienDetail,
    closeLuuNienDetail,
    changeYear,
    onYearSelectChange,
    initLuuNienYearSelect,
    _setLuuNienYear,
    _getLuuNienYear,
} = require('../js/tuvi-chart.js');

// ── Helper: mock forecast data ──
function mockForecastData(year = 2026) {
    return {
        year,
        can_chi: 'Bính Ngọ',
        nominal_age: 34,
        luu_nien: {
            menh: 'Tài Bạch',
            tu_hoa: ['Thiên Đồng Hóa Lộc', 'Thiên Cơ Hóa Quyền', 'Văn Xương Hóa Khoa', 'Liêm Trinh Hóa Kỵ'],
        },
        months: Array.from({ length: 12 }, (_, i) => ({
            month: i + 1,
            luu_nguyet_menh: ['Tài Bạch', 'Quan Lộc', 'Phúc Đức', 'Mệnh', 'Tật Ách', 'Nô Bộc',
                              'Thiên Di', 'Tài Bạch', 'Quan Lộc', 'Phúc Đức', 'Điền Trạch', 'Phu Thê'][i],
            rating: ['good', 'good', 'neutral', 'caution', 'caution', 'neutral',
                     'good', 'neutral', 'good', 'neutral', 'caution', 'good'][i],
            tu_hoa: ['Thiên Đồng Hóa Lộc'],
            key_stars: ['Tả Phù'],
        })),
    };
}

// ── Reset DOM state between tests ──
beforeEach(() => {
    jest.clearAllMocks();
    document.getElementById('ln-month-grid').innerHTML = '';
    document.getElementById('ln-month-detail').classList.add('hidden');
    document.getElementById('ln-overview').classList.add('hidden');
    document.getElementById('ln-loading').classList.add('hidden');
    document.getElementById('ln-error').classList.add('hidden');
    delete document.getElementById('ln-month-grid')._monthsData;
});

// ══════════════════════════════════════════════════════════
// Test 1: Year selector triggers re-render with new data
// ══════════════════════════════════════════════════════════
test('year selector change triggers loadYearlyForecast with new year', async () => {
    const newYear = 2027;
    _setLuuNienYear(newYear);

    const mockData = mockForecastData(newYear);
    global.fetch = jest.fn(() => Promise.resolve({
        ok: true,
        json: async () => mockData,
    }));

    // Set the select value to trigger onYearSelectChange
    const sel = document.getElementById('ln-year-select');
    sel.innerHTML = `<option value="${newYear}" selected>${newYear}</option>`;
    sel.value = String(newYear);

    await onYearSelectChange();

    expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining(`year=${newYear}`)
    );
    // After successful fetch, overview should be visible
    expect(document.getElementById('ln-overview').classList.contains('hidden')).toBe(false);
    expect(document.getElementById('ln-year-title').textContent).toContain(String(newYear));
});

// ══════════════════════════════════════════════════════════
// Test 2: 12-month grid renders exactly 12 items
// ══════════════════════════════════════════════════════════
test('month grid renders 12 items after renderYearlyForecast', () => {
    renderYearlyForecast(mockForecastData());

    const grid = document.getElementById('ln-month-grid');
    const cards = grid.querySelectorAll('.ln-month-card');
    expect(cards.length).toBe(12);

    // Verify each card has a month name
    cards.forEach((card, i) => {
        expect(card.querySelector('.ln-month-name').textContent).toContain(`Tháng ${i + 1}`);
    });
});

// ══════════════════════════════════════════════════════════
// Test 3: Clicking a month card shows detail panel
// ══════════════════════════════════════════════════════════
test('clicking month card shows detail panel with correct data', () => {
    renderYearlyForecast(mockForecastData());

    const detail = document.getElementById('ln-month-detail');
    expect(detail.classList.contains('hidden')).toBe(true);

    // Show detail for month index 0 (Tháng 1)
    showLuuNienDetail(0);

    expect(detail.classList.contains('hidden')).toBe(false);
    expect(document.getElementById('ln-detail-title').textContent).toBe('Tháng 1');

    const body = document.getElementById('ln-detail-body').textContent;
    expect(body).toContain('Lưu Nguyệt Mệnh');
    expect(body).toContain('Tài Bạch');

    // Verify active class set on first card
    const cards = document.getElementById('ln-month-grid').querySelectorAll('.ln-month-card');
    expect(cards[0].classList.contains('active')).toBe(true);
    expect(cards[1].classList.contains('active')).toBe(false);

    // Close detail
    closeLuuNienDetail();
    expect(detail.classList.contains('hidden')).toBe(true);
    expect(cards[0].classList.contains('active')).toBe(false);
});

// ══════════════════════════════════════════════════════════
// Test 4: Rating dots use correct CSS classes
// ══════════════════════════════════════════════════════════
test('rating dots apply correct CSS classes — good/neutral/caution', () => {
    renderYearlyForecast(mockForecastData());

    const cards = document.getElementById('ln-month-grid').querySelectorAll('.ln-month-card');
    // months[0].rating = 'good', months[3].rating = 'caution', months[2].rating = 'neutral'
    const dot0 = cards[0].querySelector('.ln-rating-dot');
    const dot2 = cards[2].querySelector('.ln-rating-dot');
    const dot3 = cards[3].querySelector('.ln-rating-dot');

    expect(dot0.classList.contains('good')).toBe(true);
    expect(dot2.classList.contains('neutral')).toBe(true);
    expect(dot3.classList.contains('caution')).toBe(true);

    // Verify no cross-contamination
    expect(dot0.classList.contains('caution')).toBe(false);
    expect(dot3.classList.contains('good')).toBe(false);
});
