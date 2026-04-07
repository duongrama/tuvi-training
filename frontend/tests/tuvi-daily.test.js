/**
 * Tu Vi Daily / History / Push tests — TV-FP-1, TV-FP-3, TV-FP-4
 */

// Mock navigator.serviceWorker before requiring module
Object.defineProperty(global, 'navigator', {
    value: { serviceWorker: { register: jest.fn().mockResolvedValue({ ready: Promise.resolve({}) }) } },
    configurable: true,
    writable: true,
});

// Set up minimal DOM
document.body.innerHTML = `
    <div id="daily-fortune-card" class="daily-fortune-card">
        <div id="daily-fortune-body"></div>
        <span id="daily-streak" class="hidden"></span>
        <span id="daily-palace" class="hidden"></span>
        <span id="daily-chevron">▲</span>
    </div>
    <div id="push-optin-banner" class="hidden"></div>
    <ul id="tv-history-list"></ul>
    <div id="tv-sidebar"></div>
    <div id="tv-sidebar-overlay"></div>
    <input id="day" value="15">
    <input id="month" value="3">
    <input id="year" value="1990">
    <input id="hour" value="0">
    <input id="minute" value="0">
    <input type="radio" name="gender" value="nam" checked>
    <button class="diachi-hour-btn selected" data-hour="0"></button>
    <button class="diachi-hour-btn" data-hour="2"></button>
    <button id="pill-nam" class="selected"></button>
    <button id="pill-nu"></button>
    <input id="gender-nam" type="radio" checked>
    <input id="gender-nu" type="radio">
    <div id="tuvi-share-modal" style="display:none;"></div>
    <div id="tuvi-share-preview"></div>
    <button id="btn-tuvi-share-native"></button>
    <div class="btn-share-chart"></div>
`;

// Minimal global stubs
global.getDeviceId = jest.fn().mockReturnValue('test-device-123');
global.openProfileModal = jest.fn();
global.showLoading  = jest.fn();
global.showError    = jest.fn();
global.renderChart  = jest.fn();
global.tuviApi = { getChart: jest.fn().mockResolvedValue({ cung_menh: 'Cự Môn' }) };
global.currentTuviData = { cung_menh: 'Cự Môn' };

const mod = require('../js/tuvi-daily.js');
const {
    loadDailyFortune, toggleDailyCard,
    getTuviHistory, saveTuviHistory, renderHistorySidebar,
    clearTuviHistory, reloadChart, toggleSidebar, closeSidebar,
    shareTuviChart, closeTuviShareModal,
    showPushOptIn, dismissPush,
    urlBase64ToUint8Array,
    TV_HISTORY_KEY, TV_PUSH_KEY, TV_DAILY_EXP_KEY,
} = mod;

// =========================================
// TV-FP-4: HISTORY
// =========================================

describe('getTuviHistory()', () => {
    beforeEach(() => localStorage.clear());

    test('returns empty array when nothing stored', () => {
        expect(getTuviHistory()).toEqual([]);
    });

    test('returns parsed array from localStorage', () => {
        const data = [{ id: 1, day: 15, month: 3, year: 1990 }];
        localStorage.setItem(TV_HISTORY_KEY, JSON.stringify(data));
        expect(getTuviHistory()).toEqual(data);
    });

    test('returns empty array on malformed JSON', () => {
        localStorage.setItem(TV_HISTORY_KEY, 'NOT_JSON');
        expect(getTuviHistory()).toEqual([]);
    });
});

describe('saveTuviHistory()', () => {
    const params = { day: 15, month: 3, year: 1990, hour: 0, minute: 0, gender: 'nam' };
    const chartData = { cung_menh: 'Cự Môn', nap_am: 'Kim' };

    beforeEach(() => localStorage.clear());

    test('saves entry to localStorage', () => {
        saveTuviHistory(params, chartData);
        expect(getTuviHistory()).toHaveLength(1);
        expect(getTuviHistory()[0].day).toBe(15);
    });

    test('saves menhCung from chartData.cung_menh (correct API field)', () => {
        saveTuviHistory(params, { cung_menh: 'Cự Môn' });
        expect(getTuviHistory()[0].menhCung).toBe('Cự Môn');
    });

    test('empty menhCung when cung_menh absent', () => {
        saveTuviHistory(params, {});
        expect(getTuviHistory()[0].menhCung).toBe('');
    });

    test('prepends new entries (most recent first)', () => {
        saveTuviHistory({ ...params, year: 1990 }, chartData);
        saveTuviHistory({ ...params, year: 1985 }, chartData);
        expect(getTuviHistory()[0].year).toBe(1985);
    });

    test('deduplicates same params', () => {
        saveTuviHistory(params, chartData);
        saveTuviHistory(params, { menh_cung: 'Tử Vi' });
        expect(getTuviHistory()).toHaveLength(1);
    });

    test('caps at 10 entries', () => {
        for (let y = 1970; y <= 1985; y++) {
            saveTuviHistory({ ...params, year: y }, chartData);
        }
        expect(getTuviHistory()).toHaveLength(10);
    });

    test('label is day/month/year format', () => {
        saveTuviHistory(params, chartData);
        expect(getTuviHistory()[0].label).toBe('15/3/1990');
    });
});

describe('renderHistorySidebar()', () => {
    beforeEach(() => {
        localStorage.clear();
        document.getElementById('tv-history-list').innerHTML = '';
    });

    test('shows empty message when no history', () => {
        renderHistorySidebar();
        expect(document.getElementById('tv-history-list').textContent).toContain('Chưa có lịch sử');
    });

    test('renders one item per history entry', () => {
        const p = { day: 1, month: 1, year: 2000, hour: 0, minute: 0, gender: 'nam' };
        saveTuviHistory(p, { menh_cung: 'Cự Môn' });
        saveTuviHistory({ ...p, year: 1999 }, {});
        renderHistorySidebar();
        expect(document.querySelectorAll('.tv-history-item')).toHaveLength(2);
    });

    test('shows date label in history item', () => {
        saveTuviHistory({ day: 15, month: 3, year: 1990, hour: 0, minute: 0, gender: 'nam' }, {});
        renderHistorySidebar();
        expect(document.querySelector('.tv-history-label').textContent).toBe('15/3/1990');
    });

    test('shows ☉ for nam', () => {
        saveTuviHistory({ day: 1, month: 1, year: 2000, hour: 0, minute: 0, gender: 'nam' }, {});
        renderHistorySidebar();
        expect(document.querySelector('.tv-history-gender').textContent).toContain('☉');
    });

    test('shows ☽ for nu', () => {
        saveTuviHistory({ day: 1, month: 1, year: 2000, hour: 0, minute: 0, gender: 'nu' }, {});
        renderHistorySidebar();
        expect(document.querySelector('.tv-history-gender').textContent).toContain('☽');
    });
});

describe('clearTuviHistory()', () => {
    beforeEach(() => {
        localStorage.clear();
        global.confirm = jest.fn().mockReturnValue(true);
    });

    test('clears localStorage when confirmed', () => {
        saveTuviHistory({ day: 1, month: 1, year: 2000, hour: 0, minute: 0, gender: 'nam' }, {});
        clearTuviHistory();
        expect(getTuviHistory()).toEqual([]);
    });

    test('does not clear when confirm=false', () => {
        global.confirm = jest.fn().mockReturnValue(false);
        saveTuviHistory({ day: 1, month: 1, year: 2000, hour: 0, minute: 0, gender: 'nam' }, {});
        clearTuviHistory();
        expect(getTuviHistory()).toHaveLength(1);
    });
});

describe('reloadChart()', () => {
    beforeEach(() => {
        localStorage.clear();
        global.tuviApi.getChart.mockResolvedValue({ menh_cung: 'Cự Môn' });
        global.renderChart.mockClear();
        global.showLoading.mockClear();
    });

    test('does nothing for unknown id', async () => {
        await reloadChart(999);
        expect(global.tuviApi.getChart).not.toHaveBeenCalled();
    });

    test('calls tuviApi.getChart with saved params', async () => {
        const params = { day: 15, month: 3, year: 1990, hour: 0, minute: 0, gender: 'nam' };
        saveTuviHistory(params, {});
        const entry = getTuviHistory()[0];
        await reloadChart(entry.id);
        expect(global.tuviApi.getChart).toHaveBeenCalledWith(1990, 3, 15, 0, 0, false, 'nam');
    });

    test('fills form inputs with saved params', async () => {
        const params = { day: 20, month: 6, year: 1995, hour: 8, minute: 0, gender: 'nam' };
        saveTuviHistory(params, {});
        const entry = getTuviHistory()[0];
        await reloadChart(entry.id);
        expect(document.getElementById('day').value).toBe('20');
        expect(document.getElementById('month').value).toBe('6');
        expect(document.getElementById('year').value).toBe('1995');
    });
});

describe('toggleSidebar() / closeSidebar()', () => {
    beforeEach(() => {
        document.getElementById('tv-sidebar').className = '';
        document.getElementById('tv-sidebar-overlay').className = '';
    });

    test('toggleSidebar adds open class', () => {
        toggleSidebar();
        expect(document.getElementById('tv-sidebar').classList.contains('open')).toBe(true);
    });

    test('toggleSidebar removes open class when already open', () => {
        document.getElementById('tv-sidebar').classList.add('open');
        toggleSidebar();
        expect(document.getElementById('tv-sidebar').classList.contains('open')).toBe(false);
    });

    test('closeSidebar removes open from both sidebar and overlay', () => {
        document.getElementById('tv-sidebar').classList.add('open');
        document.getElementById('tv-sidebar-overlay').classList.add('open');
        closeSidebar();
        expect(document.getElementById('tv-sidebar').classList.contains('open')).toBe(false);
        expect(document.getElementById('tv-sidebar-overlay').classList.contains('open')).toBe(false);
    });
});

// =========================================
// TV-FP-3: PUSH OPT-IN
// =========================================

describe('showPushOptIn()', () => {
    beforeEach(() => {
        localStorage.clear();
        document.getElementById('push-optin-banner').className = 'hidden';
    });

    test('shows banner when no push decision made', () => {
        showPushOptIn();
        expect(document.getElementById('push-optin-banner').classList.contains('hidden')).toBe(false);
    });

    test('does NOT show banner when already granted', () => {
        localStorage.setItem(TV_PUSH_KEY, 'granted');
        showPushOptIn();
        expect(document.getElementById('push-optin-banner').classList.contains('hidden')).toBe(true);
    });

    test('does NOT show banner when dismissed', () => {
        localStorage.setItem(TV_PUSH_KEY, 'dismissed');
        showPushOptIn();
        expect(document.getElementById('push-optin-banner').classList.contains('hidden')).toBe(true);
    });
});

describe('dismissPush()', () => {
    beforeEach(() => {
        localStorage.clear();
        document.getElementById('push-optin-banner').className = '';
    });

    test('stores dismissed in localStorage', () => {
        dismissPush();
        expect(localStorage.getItem(TV_PUSH_KEY)).toBe('dismissed');
    });

    test('hides the banner', () => {
        dismissPush();
        expect(document.getElementById('push-optin-banner').classList.contains('hidden')).toBe(true);
    });
});

// =========================================
// TV-FP-1: DAILY FORTUNE
// =========================================

describe('loadDailyFortune()', () => {
    beforeEach(() => {
        localStorage.clear();
        global.fetch = jest.fn();
        document.getElementById('daily-fortune-body').innerHTML = '';
        document.getElementById('daily-streak').className = 'hidden';
        document.getElementById('daily-palace').className = 'hidden';
        document.getElementById('daily-fortune-card').className = 'daily-fortune-card';
    });

    test('shows no_profile prompt when API returns no_profile', async () => {
        global.fetch.mockResolvedValue({ json: async () => ({ error: 'no_profile' }) });
        await loadDailyFortune();
        expect(document.getElementById('daily-fortune-body').textContent).toContain('Nhập ngày sinh');
    });

    test('shows fortune text on success', async () => {
        global.fetch.mockResolvedValue({
            json: async () => ({ fortune_text: 'Vận may đến hôm nay.', streak_count: 3, palace_name: 'Quan Lộc' })
        });
        await loadDailyFortune();
        expect(document.getElementById('daily-fortune-body').textContent).toContain('Vận may');
    });

    test('shows streak badge on success', async () => {
        global.fetch.mockResolvedValue({
            json: async () => ({ fortune_text: 'Test', streak_count: 7, palace_name: 'Mệnh' })
        });
        await loadDailyFortune();
        expect(document.getElementById('daily-streak').textContent).toContain('7');
        expect(document.getElementById('daily-streak').classList.contains('hidden')).toBe(false);
    });

    test('shows palace label on success', async () => {
        global.fetch.mockResolvedValue({
            json: async () => ({ fortune_text: 'Test', streak_count: 1, palace_name: 'Tài Bạch' })
        });
        await loadDailyFortune();
        expect(document.getElementById('daily-palace').textContent).toContain('Tài Bạch');
    });

    test('shows error message on network failure', async () => {
        global.fetch.mockRejectedValue(new Error('network'));
        await loadDailyFortune();
        expect(document.getElementById('daily-fortune-body').textContent).toContain('Không thể tải');
    });

    test('starts collapsed on second visit (localStorage flag set)', async () => {
        localStorage.setItem(TV_DAILY_EXP_KEY, '1');
        global.fetch.mockResolvedValue({
            json: async () => ({ fortune_text: 'Test', streak_count: 1, palace_name: 'Mệnh' })
        });
        await loadDailyFortune();
        expect(document.getElementById('daily-fortune-card').classList.contains('collapsed')).toBe(true);
    });
});

describe('toggleDailyCard()', () => {
    beforeEach(() => {
        document.getElementById('daily-fortune-card').className = 'daily-fortune-card';
        document.getElementById('daily-chevron').textContent = '▲';
    });

    test('adds collapsed class and changes chevron to ▼', () => {
        toggleDailyCard();
        expect(document.getElementById('daily-fortune-card').classList.contains('collapsed')).toBe(true);
        expect(document.getElementById('daily-chevron').textContent).toBe('▼');
    });

    test('removes collapsed on second toggle', () => {
        toggleDailyCard();
        toggleDailyCard();
        expect(document.getElementById('daily-fortune-card').classList.contains('collapsed')).toBe(false);
        expect(document.getElementById('daily-chevron').textContent).toBe('▲');
    });
});

// =========================================
// TV-FP-2: SHARE
// =========================================

describe('shareTuviChart()', () => {
    beforeEach(() => {
        global.fetch = jest.fn();
        document.getElementById('tuvi-share-modal').style.display = 'none';
        document.getElementById('tuvi-share-preview').innerHTML = '';
    });

    test('calls POST /api/tuvi/share with chart_data', async () => {
        global.fetch.mockResolvedValue({
            ok: true,
            json: async () => ({ story: '/shared/shares/test.png', card: '/shared/shares/test_card.png' })
        });
        await shareTuviChart();
        expect(global.fetch).toHaveBeenCalledWith('/api/tuvi/share', expect.objectContaining({ method: 'POST' }));
    });

    test('shows modal on success', async () => {
        global.fetch.mockResolvedValue({
            ok: true,
            json: async () => ({ story: '/shared/shares/test.png' })
        });
        await shareTuviChart();
        expect(document.getElementById('tuvi-share-modal').style.display).toBe('flex');
    });

    test('shows preview image on success', async () => {
        global.fetch.mockResolvedValue({
            ok: true,
            json: async () => ({ story: '/shared/shares/test.png' })
        });
        await shareTuviChart();
        expect(document.getElementById('tuvi-share-preview').innerHTML).toContain('img');
    });

    test('shows alert on API error', async () => {
        global.fetch.mockResolvedValue({ ok: false });
        global.alert = jest.fn();
        await shareTuviChart();
        expect(global.alert).toHaveBeenCalled();
    });
});

describe('closeTuviShareModal()', () => {
    test('hides the share modal', () => {
        document.getElementById('tuvi-share-modal').style.display = 'flex';
        closeTuviShareModal();
        expect(document.getElementById('tuvi-share-modal').style.display).toBe('none');
    });
});

// =========================================
// Utility
// =========================================
describe('urlBase64ToUint8Array()', () => {
    test('returns a Uint8Array', () => {
        expect(urlBase64ToUint8Array('AAAA')).toBeInstanceOf(Uint8Array);
    });

    test('handles URL-safe base64 characters (- and _)', () => {
        const result = urlBase64ToUint8Array('AAAA-AAAA_AAAA');
        expect(result).toBeInstanceOf(Uint8Array);
    });
});
