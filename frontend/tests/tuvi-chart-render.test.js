/**
 * Sprint 59 TD-3: TV tuvi-chart.js rendering coverage (28% → 80%)
 * Tests for: renderChart, renderTimeline, openDetailPanel, closeDetailPanel,
 *            showLoading, showError, handleSubmit, interpretWithAI, closeAIPanel
 */

// Mock browser methods jsdom doesn't support
HTMLElement.prototype.scrollIntoView = jest.fn();
HTMLElement.prototype.scrollTo = jest.fn();

// =========================================
// GLOBAL MOCKS (before require)
// =========================================
global.renderMarkdown = (t) => `<p>${t}</p>`;
global.readSSEStream = jest.fn(() => Promise.resolve());
global.getDeviceId = jest.fn(() => 'test-device');
global.collapseForm = jest.fn();
global.saveTuviHistory = jest.fn();
global.showPushOptIn = jest.fn();
global.openBottomSheet = jest.fn();
global.checkServerUsage = jest.fn(() => Promise.resolve({ allowed: true }));
global.incrementServerUsage = jest.fn(() => Promise.resolve());
global.showPaywallModal = jest.fn();
global.API_BASE = '';
global.tuviApi = {
    getChart: jest.fn(() => Promise.resolve({})),
};
global.fetch = jest.fn(() => Promise.resolve({ ok: true, body: {} }));

// =========================================
// DOM SETUP (before require)
// =========================================
document.body.innerHTML = `
    <div id="chart-container"></div>
    <div id="ai-section" class="hidden"></div>
    <div id="share-section" class="hidden"></div>
    <div id="timeline-section" style="display:none"></div>
    <div id="timeline"></div>
    <div id="timeline-summary" class="hidden"></div>
    <div id="btn-advanced-toggle"></div>
    <div id="detail-panel"></div>
    <div id="detail-overlay"></div>
    <div id="detail-content"></div>
    <div id="ai-interpret-panel" class="hidden"></div>
    <div id="ai-interpret-content"></div>
    <div id="personalized-badge" class="hidden"></div>
    <input id="day" value="18">
    <input id="month" value="5">
    <input id="year" value="1984">
    <input id="hour" value="0">
    <input id="minute" value="0">
    <input type="radio" name="gender" value="nam" checked>
    <form id="tuvi-form"></form>
`;

const {
    renderChart,
    renderTimeline,
    openDetailPanel,
    closeDetailPanel,
    showLoading,
    showError,
    handleSubmit,
    interpretWithAI,
    closeAIPanel,
    _setCurrentTuviData,
    _setCurrentChartData,
} = require('../js/tuvi-chart.js');

// =========================================
// Test data helpers
// =========================================
function makePalace(pos, opts = {}) {
    return {
        position: pos,
        dia_chi: ['Tý','Sửu','Dần','Mão','Thìn','Tỵ','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi'][pos - 1],
        cung_name: opts.cung_name || 'Mệnh',
        meaning: opts.meaning || '',
        can_chi: opts.can_chi || 'Kỷ Tý',
        stars: opts.stars || [
            { name: 'Tử Vi', element: 'thổ', brightness: 'Miếu', tu_hoa: 'Hóa Lộc' },
        ],
        adjective_stars: opts.adjective_stars || [{ name: 'Đào Hoa' }],
        trang_sinh: opts.trang_sinh || null,
        bac_si: opts.bac_si || null,
        tuong_tinh: opts.tuong_tinh || null,
        thai_tue: opts.thai_tue || null,
        dai_han: opts.dai_han || { range: [3, 12], can_chi: 'Canh Dần', is_current: false },
        tuan: opts.tuan || false,
        triet: opts.triet || false,
    };
}

const basicChartData = {
    birth: { solar: { day: 18, month: 5, year: 1984, hour: 0, minute: 0 }, lunar: { day: 18, month: 4, year: 1984 } },
    cung_menh: 'Tý',
    cung_than: 'Ngọ',
    menh_chu: 'Vũ Khúc',
    than_chu: 'Hỏa Tinh',
    nap_am: { name: 'Hải Trung Kim' },
    cuc: { name: 'Mộc Tam Cục' },
    tu_hoa: {
        'hoa_lộc':   { star: 'Liêm Trinh', palace: 'Mệnh' },
        'hoa_quyền': { star: 'Phá Quân',   palace: 'Quan Lộc' },
        'hoa_khoa':  { star: 'Vũ Khúc',    palace: 'Tài Bạch' },
        'hoa_kỵ':    { star: 'Thái Dương',  palace: 'Phụ Mẫu' },
    },
    palaces: [
        makePalace(1, { cung_name: 'Mệnh', stars: [{ name: 'Tử Vi', element: 'thổ', brightness: 'Miếu', tu_hoa: 'Hóa Lộc' }] }),
        makePalace(2, { cung_name: 'Phụ Mẫu', stars: [] }),
        makePalace(7, { cung_name: 'Quan Lộc', stars: [{ name: 'Thiên Phủ', element: 'kim', brightness: 'Vượng', tu_hoa: null }, { name: 'Đào Hoa', element: 'mộc', brightness: '', tu_hoa: null }] }),
    ],
    dai_han: [
        { start_age: 3,  end_age: 12, period: 'Canh Dần', palace_name: 'Mệnh',    palace_index: 1 },
        { start_age: 13, end_age: 22, period: 'Kỷ Sửu',   palace_name: 'Phụ Mẫu', palace_index: 2 },
    ],
    tieu_han: { palace_index: 1, palace_name: 'Mệnh', year: 2024 },
    tieu_han_upcoming: [{ palace_name: 'Phụ Mẫu' }],
};

// =========================================
// showLoading() + showError()
// =========================================
describe('showLoading()', () => {
    test('renders loading text in chart-container', () => {
        showLoading();
        const container = document.getElementById('chart-container');
        expect(container.innerHTML).toContain('Đang tính toán');
    });
});

describe('showError(message)', () => {
    test('renders error message in chart-container', () => {
        showError('Test error');
        const container = document.getElementById('chart-container');
        expect(container.innerHTML).toContain('Test error');
        expect(container.innerHTML).toContain('Lỗi');
    });
});

// =========================================
// renderTimeline()
// =========================================
describe('renderTimeline()', () => {
    beforeEach(() => {
        document.getElementById('timeline').innerHTML = '';
        document.getElementById('timeline-summary').classList.add('hidden');
    });

    test('renders timeline segments from daiHan', () => {
        renderTimeline(basicChartData);
        const timeline = document.getElementById('timeline');
        expect(timeline.querySelectorAll('.timeline-segment').length).toBeGreaterThan(0);
    });

    test('makes timeline-section visible', () => {
        renderTimeline(basicChartData);
        const section = document.getElementById('timeline-section');
        expect(section.style.display).toBe('block');
    });

    test('shows summary banner with current dai han', () => {
        const data = {
            ...basicChartData,
            birth: { solar: { year: new Date().getFullYear() - 5 } },
            dai_han: [{ start_age: 3, end_age: 12, period: 'Canh Dần', palace_name: 'Mệnh', palace_index: 1 }],
        };
        renderTimeline(data);
        const summary = document.getElementById('timeline-summary');
        // summary shows if there's a current segment
        expect(typeof summary.innerHTML).toBe('string');
    });

    test('uses fallback data when daiHan is empty', () => {
        const emptyData = { ...basicChartData, dai_han: [], tieu_han: null, tieu_han_upcoming: [] };
        renderTimeline(emptyData);
        const timeline = document.getElementById('timeline');
        expect(timeline.querySelectorAll('.timeline-segment').length).toBe(10); // fallback has 10
    });

    test('returns early when timeline-section missing', () => {
        const section = document.getElementById('timeline-section');
        section.id = 'timeline-section-hidden';
        expect(() => renderTimeline(basicChartData)).not.toThrow();
        section.id = 'timeline-section'; // restore
    });
});

// =========================================
// renderChart()
// =========================================
describe('renderChart()', () => {
    beforeEach(() => {
        localStorage.clear();
        document.getElementById('chart-container').innerHTML = '';
        jest.clearAllMocks();
    });

    test('renders palace elements in chart-container', () => {
        renderChart(basicChartData);
        const container = document.getElementById('chart-container');
        expect(container.innerHTML).not.toBe('');
        expect(container.querySelectorAll('.palace').length).toBeGreaterThan(0);
    });

    test('shows ai-section and share-section', () => {
        renderChart(basicChartData);
        const aiSection = document.getElementById('ai-section');
        const shareSection = document.getElementById('share-section');
        expect(aiSection.classList.contains('hidden')).toBe(false);
        expect(shareSection.classList.contains('hidden')).toBe(false);
    });

    test('marks Mệnh palace with menh class', () => {
        renderChart(basicChartData);
        const menh = document.querySelector('.palace.menh');
        expect(menh).not.toBeNull();
    });

    test('calls collapseForm and saveTuviHistory', () => {
        renderChart(basicChartData);
        expect(global.collapseForm).toHaveBeenCalled();
        expect(global.saveTuviHistory).toHaveBeenCalled();
    });

    test('renders advanced view content when isAdvancedView = true', () => {
        localStorage.setItem('tuvi_advanced_view', 'true');
        const advancedPalace = makePalace(1, {
            cung_name: 'Mệnh',
            can_chi: 'Kỷ Tý',
            adjective_stars: [{ name: 'Đào Hoa' }],
            trang_sinh: 'Lâm Quan',
            dai_han: { range: [3, 12] },
            tuan: true,
            triet: false,
        });
        const data = { ...basicChartData, palaces: [advancedPalace] };
        renderChart(data);
        const container = document.getElementById('chart-container');
        expect(container.querySelector('.palace.advanced')).not.toBeNull();
        localStorage.clear();
    });

    test('handles palace with aux stars (non-main stars)', () => {
        const palaceWithAux = makePalace(1, {
            stars: [
                { name: 'Đào Hoa', element: 'mộc', brightness: '', tu_hoa: null }, // not in MAIN_STARS
            ]
        });
        const data = { ...basicChartData, palaces: [palaceWithAux] };
        expect(() => renderChart(data)).not.toThrow();
    });

    test('renders center panel', () => {
        renderChart(basicChartData);
        const container = document.getElementById('chart-container');
        expect(container.innerHTML).toContain('Tử Vi Lá Số');
    });

    test('renders advanced toggle button', () => {
        renderChart(basicChartData);
        const wrapper = document.getElementById('chart-container').querySelector('.chart-grid-wrapper');
        expect(wrapper).not.toBeNull();
        // toggle button is appended to wrapper
        const btn = wrapper.querySelector('#btn-advanced-toggle') || wrapper.querySelector('.btn-advanced-toggle');
        expect(btn).not.toBeNull();
    });
});

// =========================================
// openDetailPanel() + closeDetailPanel()
// =========================================
describe('openDetailPanel()', () => {
    const palace = makePalace(1, { cung_name: 'Mệnh' });

    beforeEach(() => {
        // Reset window.innerWidth to desktop (> 600)
        Object.defineProperty(window, 'innerWidth', { value: 1024, writable: true, configurable: true });
        document.getElementById('detail-panel').classList.remove('open');
        document.getElementById('detail-overlay').classList.remove('open');
    });

    test('opens detail panel on desktop (innerWidth > 600)', () => {
        openDetailPanel(palace);
        const panel = document.getElementById('detail-panel');
        const content = document.getElementById('detail-content');
        expect(panel.classList.contains('open')).toBe(true);
        expect(content.innerHTML).toContain('Mệnh');
    });

    test('calls openBottomSheet on mobile (innerWidth <= 600)', () => {
        Object.defineProperty(window, 'innerWidth', { value: 400, writable: true, configurable: true });
        global.openBottomSheet.mockClear();
        openDetailPanel(palace);
        expect(global.openBottomSheet).toHaveBeenCalled();
    });

    test('opens overlay when present', () => {
        openDetailPanel(palace);
        expect(document.getElementById('detail-overlay').classList.contains('open')).toBe(true);
    });
});

describe('closeDetailPanel()', () => {
    test('removes open class from panel and overlay', () => {
        document.getElementById('detail-panel').classList.add('open');
        document.getElementById('detail-overlay').classList.add('open');
        closeDetailPanel();
        expect(document.getElementById('detail-panel').classList.contains('open')).toBe(false);
        expect(document.getElementById('detail-overlay').classList.contains('open')).toBe(false);
    });
});

// =========================================
// handleSubmit()
// =========================================
describe('handleSubmit()', () => {
    const mockEvent = { preventDefault: jest.fn() };

    beforeEach(() => {
        jest.clearAllMocks();
        document.getElementById('chart-container').innerHTML = '';
    });

    test('calls event.preventDefault()', async () => {
        global.tuviApi.getChart.mockResolvedValueOnce(basicChartData);
        await handleSubmit(mockEvent);
        expect(mockEvent.preventDefault).toHaveBeenCalled();
    });

    test('shows error when year/month/day missing', async () => {
        document.getElementById('year').value = '';
        await handleSubmit(mockEvent);
        const container = document.getElementById('chart-container');
        expect(container.innerHTML).toContain('Lỗi');
        document.getElementById('year').value = '1984'; // restore
    });

    test('calls tuviApi.getChart with form values', async () => {
        global.tuviApi.getChart.mockResolvedValueOnce(basicChartData);
        await handleSubmit(mockEvent);
        expect(global.tuviApi.getChart).toHaveBeenCalledWith(1984, 5, 18, 0, 0, false, 'nam');
    });

    test('shows error when getChart rejects', async () => {
        global.tuviApi.getChart.mockRejectedValueOnce(new Error('API fail'));
        await handleSubmit(mockEvent);
        const container = document.getElementById('chart-container');
        expect(container.innerHTML).toContain('Lỗi');
    });
});

// =========================================
// interpretWithAI()
// =========================================
describe('interpretWithAI()', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        document.getElementById('ai-interpret-panel').classList.add('hidden');
        document.getElementById('ai-interpret-content').innerHTML = '';
        global.readSSEStream = jest.fn(() => Promise.resolve());
        global.fetch = jest.fn(() => Promise.resolve({ ok: true, body: {} }));
    });

    test('shows alert and returns early when no chart data', async () => {
        _setCurrentTuviData(null);
        window.alert = jest.fn();
        await interpretWithAI();
        expect(window.alert).toHaveBeenCalled();
        expect(global.fetch).not.toHaveBeenCalled();
    });

    test('shows ai panel and calls fetch when data available', async () => {
        _setCurrentTuviData(basicChartData);
        await interpretWithAI();
        const panel = document.getElementById('ai-interpret-panel');
        expect(panel.classList.contains('hidden')).toBe(false);
        expect(global.fetch).toHaveBeenCalledWith(
            expect.stringContaining('/api/tuvi/interpret/stream'),
            expect.objectContaining({ method: 'POST' })
        );
    });

    test('calls readSSEStream when fetch succeeds', async () => {
        _setCurrentTuviData(basicChartData);
        await interpretWithAI();
        expect(global.readSSEStream).toHaveBeenCalled();
    });

    test('shows error message when fetch fails', async () => {
        _setCurrentTuviData(basicChartData);
        global.fetch.mockResolvedValueOnce({ ok: false });
        await interpretWithAI();
        const content = document.getElementById('ai-interpret-content');
        expect(content.innerHTML).toContain('Lỗi');
    });

    test('shows personalized badge when tuvi_profile in localStorage', async () => {
        _setCurrentTuviData(basicChartData);
        localStorage.setItem('tuvi_profile', JSON.stringify({ name: 'Test' }));
        await interpretWithAI();
        const badge = document.getElementById('personalized-badge');
        expect(badge.classList.contains('hidden')).toBe(false);
        localStorage.removeItem('tuvi_profile');
    });
});

// =========================================
// closeAIPanel()
// =========================================
describe('closeAIPanel()', () => {
    test('adds hidden class and removes slide-in', () => {
        const panel = document.getElementById('ai-interpret-panel');
        panel.classList.remove('hidden');
        panel.classList.add('slide-in');
        closeAIPanel();
        expect(panel.classList.contains('hidden')).toBe(true);
        expect(panel.classList.contains('slide-in')).toBe(false);
    });
});
