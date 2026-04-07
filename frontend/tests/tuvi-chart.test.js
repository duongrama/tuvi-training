/**
 * Sprint 50/51: Tu Vi Chart Overhaul Phase 2 + Per-Palace Interpretation
 * Tests for: Tứ Hóa dots, center panel, advanced toggle, hover popup, TVF-5
 */

// Minimal stubs for globals required by tuvi-chart.js
global.renderMarkdown = (t) => t;
global.readSSEStream = jest.fn();
global.getDeviceId = jest.fn(() => 'test-device');
global.collapseForm = jest.fn();
global.saveTuviHistory = jest.fn();
global.showPushOptIn = jest.fn();
global.openBottomSheet = jest.fn();
global.checkServerUsage = jest.fn();
global.incrementServerUsage = jest.fn();
global.showPaywallModal = jest.fn();
global.API_BASE = '';

const {
    getTuHoaClass,
    getBrightnessClass,
    getBrightnessLabel,
    buildDetailHTML,
    buildCenterPanelHTML,
    toggleAdvancedView,
    isAdvancedView,
    getPalaceDomain,
    getPalaceButtonLabel,
    getTamHopPositions,
    interpretPalace,
    _setCurrentTuviData,
} = require('../js/tuvi-chart.js');

// =========================================
// TVF-3: Tứ Hóa class mapping
// =========================================
describe('getTuHoaClass()', () => {
    test('Hóa Lộc → loc', () => expect(getTuHoaClass('Hóa Lộc')).toBe('loc'));
    test('Hóa Quyền → quyen', () => expect(getTuHoaClass('Hóa Quyền')).toBe('quyen'));
    test('Hóa Khoa → khoa', () => expect(getTuHoaClass('Hóa Khoa')).toBe('khoa'));
    test('Hóa Kỵ → ky', () => expect(getTuHoaClass('Hóa Kỵ')).toBe('ky'));
    test('null → empty string', () => expect(getTuHoaClass(null)).toBe(''));
    test('empty → empty string', () => expect(getTuHoaClass('')).toBe(''));
});

// =========================================
// TVF-1: buildDetailHTML — extended content
// =========================================
describe('buildDetailHTML() — extended (TVF-1)', () => {
    const palace = {
        position: 1,
        dia_chi: 'Tý',
        cung_name: 'Mệnh',
        meaning: 'Ý nghĩa cung Mệnh',
        can_chi: 'Kỷ Tý',
        stars: [
            { name: 'Tử Vi', element: 'thổ', brightness: 'Miếu', tu_hoa: 'Hóa Lộc' },
            { name: 'Thiên Phủ', element: 'thổ', brightness: '', tu_hoa: null },
            { name: 'Văn Xương', element: 'kim', brightness: '', tu_hoa: null },
        ],
        adjective_stars: [
            { name: 'Đào Hoa', brightness: '' },
            { name: 'Hồng Loan', brightness: 'Miếu' },
        ],
        trang_sinh: 'Lâm Quan',
        bac_si: 'Bác Sĩ',
        tuong_tinh: 'Tuế Dịch',
        thai_tue: 'Tang Môn',
        dai_han: { range: [3, 12], can_chi: 'Canh Dần', is_current: true },
        tuan: false,
        triet: false,
    };

    let html;
    beforeEach(() => { html = buildDetailHTML(palace); });

    test('header includes can_chi + cung_name + dai_han range', () => {
        expect(html).toContain('Kỷ Tý');
        expect(html).toContain('Mệnh');
        expect(html).toContain('3');
        expect(html).toContain('12');
    });

    test('adjective stars section rendered', () => {
        expect(html).toContain('Đào Hoa');
        expect(html).toContain('Hồng Loan');
    });

    test('ring values rendered (trang_sinh, bac_si, tuong_tinh, thai_tue)', () => {
        expect(html).toContain('Lâm Quan');
        expect(html).toContain('Bác Sĩ');
        expect(html).toContain('Tuế Dịch');
        expect(html).toContain('Tang Môn');
    });

    test('Đại Hạn is_current badge shown when current', () => {
        expect(html).toContain('hiện tại');
    });

    test('Đại Hạn can_chi shown', () => {
        expect(html).toContain('Canh Dần');
    });

    test('Tuần/Triệt warnings NOT shown when both false', () => {
        expect(html).not.toContain('Tuần');
        expect(html).not.toContain('Triệt');
    });

    test('Tuần warning shown when tuan=true', () => {
        const h = buildDetailHTML({ ...palace, tuan: true });
        expect(h).toContain('Tuần');
    });

    test('Triệt warning shown when triet=true', () => {
        const h = buildDetailHTML({ ...palace, triet: true });
        expect(h).toContain('Triệt');
    });
});

// =========================================
// TVF-2: buildCenterPanelHTML
// =========================================
describe('buildCenterPanelHTML() — TVF-2', () => {
    const chartData = {
        birth: { solar: { day: 18, month: 5, year: 1984 }, lunar: { day: 18, month: 4, year: 1984 } },
        nap_am: { name: 'Hải Trung Kim' },
        cuc: { name: 'Mộc Tam Cục' },
        menh_chu: 'Vũ Khúc',
        than_chu: 'Hỏa Tinh',
        cung_menh: 'Tý',
        cung_than: 'Ngọ',
        tu_hoa: {
            'hoa_lộc':   { star: 'Liêm Trinh', palace: 'Mệnh' },
            'hoa_quyền': { star: 'Phá Quân',   palace: 'Quan Lộc' },
            'hoa_khoa':  { star: 'Vũ Khúc',    palace: 'Tài Bạch' },
            'hoa_kỵ':    { star: 'Thái Dương',  palace: 'Phụ Mẫu' },
        },
    };

    let html;
    beforeEach(() => { html = buildCenterPanelHTML(chartData); });

    test('shows Mệnh Chủ', () => expect(html).toContain('Vũ Khúc'));
    test('shows Thân Chủ', () => expect(html).toContain('Hỏa Tinh'));
    test('shows Tứ Hóa Lộc star', () => expect(html).toContain('Liêm Trinh'));
    test('shows Tứ Hóa Quyền star', () => expect(html).toContain('Phá Quân'));
    test('shows Tứ Hóa Khoa star', () => expect(html).toContain('Vũ Khúc'));
    test('shows Tứ Hóa Kỵ star', () => expect(html).toContain('Thái Dương'));
    test('shows Nạp Âm', () => expect(html).toContain('Hải Trung Kim'));
    test('shows Cục', () => expect(html).toContain('Mộc Tam Cục'));
    test('shows birth date', () => {
        expect(html).toContain('18');
        expect(html).toContain('1984');
    });

    test('graceful when tu_hoa absent', () => {
        const h = buildCenterPanelHTML({ ...chartData, tu_hoa: null });
        expect(h).toContain('Vũ Khúc'); // menh_chu still shows
    });

    test('graceful when menh_chu/than_chu absent', () => {
        const h = buildCenterPanelHTML({ ...chartData, menh_chu: null, than_chu: null });
        expect(typeof h).toBe('string');
    });
});

// =========================================
// TVF-4: Advanced View Toggle
// =========================================
describe('toggleAdvancedView() + isAdvancedView() — TVF-4', () => {
    beforeEach(() => {
        localStorage.clear();
    });

    test('isAdvancedView() returns false by default', () => {
        expect(isAdvancedView()).toBe(false);
    });

    test('toggleAdvancedView() flips state to true', () => {
        toggleAdvancedView();
        expect(isAdvancedView()).toBe(true);
    });

    test('toggleAdvancedView() persists in localStorage', () => {
        toggleAdvancedView();
        expect(localStorage.getItem('tuvi_advanced_view')).toBe('true');
    });

    test('toggleAdvancedView() twice returns to false', () => {
        toggleAdvancedView();
        toggleAdvancedView();
        expect(isAdvancedView()).toBe(false);
    });

    test('isAdvancedView() reads existing localStorage value', () => {
        localStorage.setItem('tuvi_advanced_view', 'true');
        expect(isAdvancedView()).toBe(true);
    });
});

// =========================================
// TVF-5: getPalaceDomain()
// =========================================
describe('getPalaceDomain() — TVF-5', () => {
    test('Mệnh → vận mệnh tổng quát', () => {
        expect(getPalaceDomain('Mệnh')).toContain('vận mệnh');
    });
    test('Quan Lộc → sự nghiệp', () => {
        expect(getPalaceDomain('Quan Lộc')).toContain('sự nghiệp');
    });
    test('Tài Bạch → tài chính', () => {
        expect(getPalaceDomain('Tài Bạch')).toContain('tài chính');
    });
    test('Phu Thê → tình duyên', () => {
        expect(getPalaceDomain('Phu Thê')).toContain('tình duyên');
    });
    test('unknown cung → returns cung name as fallback', () => {
        expect(getPalaceDomain('Unknown')).toBe('Unknown');
    });
});

// =========================================
// TVF-5: getTamHopPositions()
// =========================================
describe('getTamHopPositions() — TVF-5', () => {
    const nsort = (arr) => arr.sort((a, b) => a - b);
    test('pos 1 → [5, 9]', () => {
        expect(nsort(getTamHopPositions(1))).toEqual([5, 9]);
    });
    test('pos 5 → [1, 9]', () => {
        expect(nsort(getTamHopPositions(5))).toEqual([1, 9]);
    });
    test('pos 9 → [1, 5]', () => {
        expect(nsort(getTamHopPositions(9))).toEqual([1, 5]);
    });
    test('pos 2 → [6, 10]', () => {
        expect(nsort(getTamHopPositions(2))).toEqual([6, 10]);
    });
    test('pos 12 → [4, 8]', () => {
        expect(nsort(getTamHopPositions(12))).toEqual([4, 8]);
    });
    test('returns exactly 2 positions', () => {
        expect(getTamHopPositions(7)).toHaveLength(2);
    });
});

// =========================================
// TVF-5: buildDetailHTML includes interpret button
// =========================================
describe('buildDetailHTML() — TVF-5 button', () => {
    const palace = {
        position: 1,
        cung_name: 'Mệnh',
        can_chi: 'Kỷ Tý',
        stars: [],
        adjective_stars: [],
        dai_han: { range: [3, 12], can_chi: 'Canh Dần', is_current: false },
        tuan: false,
        triet: false,
    };

    test('contains Luận Giải button (palace-specific label for Mệnh)', () => {
        const html = buildDetailHTML(palace);
        expect(html).toContain('Luận Giải Mệnh');
    });

    test('button calls interpretPalace with palace position', () => {
        const html = buildDetailHTML(palace);
        expect(html).toContain('interpretPalace(1)');
    });
});

// =========================================
// TVF-5: interpretPalace() — freemium gate
// =========================================
describe('interpretPalace() — TVF-5 freemium gate', () => {
    const mockPalace = {
        position: 7,
        cung_name: 'Quan Lộc',
        can_chi: 'Canh Ngọ',
        stars: [],
        adjective_stars: [],
        meaning: '',
        dai_han: null,
        tuan: false,
        triet: false,
    };

    const mockChartData = {
        birth: { solar: { day: 18, month: 5, year: 1984, hour: 0, minute: 0, gender: 'nam' } },
        palaces: [
            mockPalace,
            { position: 1,  cung_name: 'Mệnh',   stars: [], adjective_stars: [] },
            { position: 3,  cung_name: 'Tử Tức', stars: [], adjective_stars: [] },
            { position: 11, cung_name: 'Thiên Di', stars: [], adjective_stars: [] },
        ],
        nap_am: { name: 'Hải Trung Kim' },
        cuc: { name: 'Mộc Tam Cục' },
        menh_chu: 'Vũ Khúc',
        than_chu: 'Hỏa Tinh',
        tu_hoa: null,
    };

    beforeEach(() => {
        jest.clearAllMocks();
        // Set up DOM
        document.body.innerHTML = `
            <div id="detail-content"></div>
            <div id="detail-panel"></div>
        `;
        // Set module-level chart data via exported setter
        _setCurrentTuviData(mockChartData);
        global.readSSEStream = jest.fn(() => Promise.resolve());
        global.fetch = jest.fn(() => Promise.resolve({ ok: true }));
        global.checkServerUsage = jest.fn(() => Promise.resolve({ allowed: true }));
        global.incrementServerUsage = jest.fn(() => Promise.resolve());
        global.showPaywallModal = jest.fn();
    });

    afterEach(() => {
        _setCurrentTuviData(null);
    });

    test('calls checkServerUsage before fetch', async () => {
        await interpretPalace(7);
        expect(global.checkServerUsage).toHaveBeenCalledWith('tuvi', expect.any(String));
    });

    test('shows paywall and does NOT fetch when usage not allowed', async () => {
        global.checkServerUsage = jest.fn(() => Promise.resolve({ allowed: false }));
        await interpretPalace(7);
        expect(global.showPaywallModal).toHaveBeenCalled();
        expect(global.fetch).not.toHaveBeenCalled();
    });

    test('calls readSSEStream when usage allowed', async () => {
        await interpretPalace(7);
        expect(global.readSSEStream).toHaveBeenCalled();
    });

    test('does nothing if currentTuviData is null', async () => {
        _setCurrentTuviData(null);
        await interpretPalace(7);
        expect(global.fetch).not.toHaveBeenCalled();
    });
});

// =========================================
// TPD-2: getPalaceButtonLabel() — all 12 palaces
// =========================================
describe('getPalaceButtonLabel() — TPD-2', () => {
    test('Tật Ách → Luận Giải Sức Khỏe', () => expect(getPalaceButtonLabel('Tật Ách')).toBe('Luận Giải Sức Khỏe'));
    test('Tử Tức → Luận Giải Con Cái',   () => expect(getPalaceButtonLabel('Tử Tức')).toBe('Luận Giải Con Cái'));
    test('Phụ Mẫu → Luận Giải Phụ Mẫu', () => expect(getPalaceButtonLabel('Phụ Mẫu')).toBe('Luận Giải Phụ Mẫu'));
    test('Huynh Đệ → Luận Giải Huynh Đệ', () => expect(getPalaceButtonLabel('Huynh Đệ')).toBe('Luận Giải Huynh Đệ'));
    test('Nô Bộc → Luận Giải Giao Tế',   () => expect(getPalaceButtonLabel('Nô Bộc')).toBe('Luận Giải Giao Tế'));
    test('Thiên Di → Luận Giải Xuất Hành', () => expect(getPalaceButtonLabel('Thiên Di')).toBe('Luận Giải Xuất Hành'));
    test('Điền Trạch → Luận Giải Nhà Cửa', () => expect(getPalaceButtonLabel('Điền Trạch')).toBe('Luận Giải Nhà Cửa'));
    test('Phúc Đức → Luận Giải Phúc Đức', () => expect(getPalaceButtonLabel('Phúc Đức')).toBe('Luận Giải Phúc Đức'));
    test('Mệnh → Luận Giải Mệnh',         () => expect(getPalaceButtonLabel('Mệnh')).toBe('Luận Giải Mệnh'));
    test('Quan Lộc → Luận Giải Sự Nghiệp', () => expect(getPalaceButtonLabel('Quan Lộc')).toBe('Luận Giải Sự Nghiệp'));
    test('Phu Thê → Luận Giải Tình Duyên', () => expect(getPalaceButtonLabel('Phu Thê')).toBe('Luận Giải Tình Duyên'));
    test('Tài Bạch → Luận Giải Tài Lộc',  () => expect(getPalaceButtonLabel('Tài Bạch')).toBe('Luận Giải Tài Lộc'));
    test('unknown → fallback Luận Giải Cung Này', () => expect(getPalaceButtonLabel('Unknown')).toBe('Luận Giải Cung Này'));

    test('buildDetailHTML button uses palace-specific label', () => {
        const h = buildDetailHTML({ position: 1, cung_name: 'Tật Ách', stars: [], adjective_stars: [], tuan: false, triet: false });
        expect(h).toContain('Luận Giải Sức Khỏe');
    });
});
