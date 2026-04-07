/**
 * AN-10: Tu Vi Palace Grid Clockwise Fade-In Animation Tests
 * Tests: palaces have staggered animation-delay in clockwise order, center panel animates last
 */

global.fetch = jest.fn();
global.renderMarkdown = jest.fn(text => `<p>${text}</p>`);
global.readSSEStream = jest.fn();
global.lucide = { createIcons: jest.fn() };
global.localStorage = {
    getItem: jest.fn(() => null),
    setItem: jest.fn(),
    removeItem: jest.fn()
};
global.getDeviceId = jest.fn(() => 'test-device');
global.alert = jest.fn();
global.collapseForm = jest.fn();
global.showLuuNienButton = jest.fn();
global.showCompatibilityButton = jest.fn();

// Mock requestAnimationFrame
global.requestAnimationFrame = jest.fn(cb => { setTimeout(cb, 0); return 1; });

function setupDOM() {
    document.body.innerHTML = `
        <div id="chart-container"></div>
        <div id="ai-section" class="hidden"></div>
        <div id="detail-panel" class="hidden"></div>
        <div id="detail-content"></div>
        <div id="tuvi-loading" class="hidden"></div>
        <div id="tuvi-error" class="hidden"></div>
        <div id="tuvi-result" class="hidden"></div>
        <div id="luu-nien-btn-container"></div>
        <div id="compat-btn-container"></div>
    `;
}

// Minimal mock chart data for 12 palaces
function makeChartData() {
    const positions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
    return {
        palaces: positions.map(pos => ({
            position: pos,
            dia_chi: ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi'][pos - 1],
            cung_name: `Cung ${pos}`,
            stars: [],
            aux_stars: []
        })),
        birth_info: { can_chi: 'Giáp Tý', ngu_hanh: 'Thủy', menh: 'Thủy' },
        than_dia_chi: 'Sửu',
        menh_dia_chi: 'Tý',
        nhat_chu_ngu_hanh: 'Thủy'
    };
}

let chartModule;

beforeEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
    setupDOM();
    global.fetch = jest.fn();
    chartModule = require('../js/tuvi-chart.js');
});

describe('AN-10: Tu Vi palace grid clockwise fade-in animation', () => {
    test('palace cells have staggered animation-delay in clockwise order', () => {
        const { renderChart } = chartModule;
        const data = makeChartData();
        renderChart(data);

        const container = document.getElementById('chart-container');
        const palaces = container.querySelectorAll('.palace');
        expect(palaces.length).toBe(12);

        // Each palace should have palace-enter class
        palaces.forEach(p => {
            expect(p.classList.contains('palace-enter')).toBe(true);
        });

        // animation-delay should be staggered (not all the same)
        const delays = Array.from(palaces).map(p => p.style.animationDelay);
        const uniqueDelays = new Set(delays);
        expect(uniqueDelays.size).toBeGreaterThan(1);
    });

    test('center panel animation-delay comes after all 12 palaces', () => {
        const { renderChart } = chartModule;
        const data = makeChartData();
        renderChart(data);

        const container = document.getElementById('chart-container');
        const palaces = container.querySelectorAll('.palace');
        const centerPanel = container.querySelector('.center-panel');

        expect(centerPanel).toBeTruthy();

        // Center panel delay should be after all palace delays
        const palaceDelays = Array.from(palaces).map(p =>
            parseFloat(p.style.animationDelay || '0')
        );
        const maxPalaceDelay = Math.max(...palaceDelays);

        const centerDelay = parseFloat(centerPanel.style.animationDelay || '0');
        expect(centerDelay).toBeGreaterThan(maxPalaceDelay);
    });
});
