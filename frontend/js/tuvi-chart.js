// Tử Vi Chart Renderer — Sprint 39 UX Revamp

// SEO-1: Update OG meta tags dynamically for social sharing
async function updateOgMeta(readingId) {
    try {
        const res = await fetch(`${API_BASE}/api/og-meta?reading_id=${encodeURIComponent(readingId)}`);
        if (!res.ok) return;
        const data = await res.json();
        const setMeta = (prop, val) => {
            const el = document.querySelector(`meta[property="${prop}"]`);
            if (el && val) el.setAttribute('content', val);
        };
        setMeta('og:title', data.title);
        setMeta('og:description', data.description);
        setMeta('og:image', data.image_url);
    } catch (e) {
        // Non-critical — ignore OG update errors
    }
}


// =========================================
// PALACE GRID — 4x4 standard layout (R2 fix)
// =========================================
const PALACE_GRID = {
    6:  { row: 1, col: 1 },  // Tỵ
    7:  { row: 1, col: 2 },  // Ngọ
    8:  { row: 1, col: 3 },  // Mùi
    9:  { row: 1, col: 4 },  // Thân
    5:  { row: 2, col: 1 },  // Thìn
    10: { row: 2, col: 4 },  // Dậu
    4:  { row: 3, col: 1 },  // Mão  (was Tuất/Dậu mismatch — corrected)
    11: { row: 3, col: 4 },  // Tuất
    3:  { row: 4, col: 1 },  // Dần
    2:  { row: 4, col: 2 },  // Sửu
    1:  { row: 4, col: 3 },  // Tý  (FIXED from row 5)
    12: { row: 4, col: 4 }   // Hợi (FIXED from row 5)
};

// Clockwise order for staggered animation: Tỵ→Ngọ→Mùi→Thân→Dậu→Tuất→Hợi→Tý→Sửu→Dần→Mão→Thìn
const CLOCKWISE_ORDER = [6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5];


// Main stars (14 chính tinh)
const MAIN_STARS = new Set([
    'Tử Vi', 'Thiên Phủ', 'Thái Dương', 'Thái Âm', 'Liêm Trinh',
    'Tham Lang', 'Cự Môn', 'Thiên Tướng', 'Vũ Khúc', 'Thiên Đồng',
    'Thiên Cơ', 'Thiên Lương', 'Thất Sát', 'Phá Quân'
]);

// Sát tinh (bad stars) — displayed on the right side of each palace cell
// Source: dieu chinh cac sao phu tinh.pdf (right column)
const BAD_STARS = new Set([
    // Tứ Sát + Không Kiếp
    'Kình Dương', 'Đà La', 'Hỏa Tinh', 'Linh Tinh', 'Địa Không', 'Địa Kiếp',
    // Hung tinh
    'Thiên Hình', 'Thiên Diêu', 'Phá Toái', 'Phi Liêm',
    'Thiên Khốc', 'Thiên Hư', 'Thiên Không',
    // Hao tinh + VN renamed
    'Tiểu Hao', 'Đại Hao', 'Tử Phù', 'Tuế Phá',
    // Vòng Thái Tuế sát khí
    'Thái Tuế', 'Bạch Hổ', 'Tang Môn', 'Điếu Khách',
    'Quan Phù', 'Quan Phủ', 'Bệnh Phù', 'Phục Binh',
    // Sát khí khác
    'Kiếp Sát', 'Cô Thần', 'Quả Tú', 'Tuần Không', 'Triệt Lộ',
    'Địa Võng', 'Thiên Thương', 'Thiên Sứ', 'Thiên La', 'Lưu Hà', 'Hóa Kỵ',
    // Giữ thêm các sao hung không trong PDF
    'Tai Sát', 'Thiên Sát', 'Nguyệt Sát', 'Vong Thần',
]);

// Hành của các phụ tinh / adjective stars (để tô màu)
// Source: dieu chinh cac sao phu tinh.pdf — màu xám=kim, đen=thủy, đỏ=hỏa, xanh=mộc, vàng=thổ
const STAR_ELEMENT_MAP = {
    // ── Kim — xám ────────────────────────────────────────────────────────────
    'Văn Xương': 'kim', 'Hóa Khoa': 'kim',
    'Thai Phụ': 'kim', 'Hoa Cái': 'kim',
    'Quan Đới': 'kim', 'Lâm Quan': 'kim', 'Đế Vượng': 'kim',
    'Tấu Thư': 'kim', 'Bạch Hổ': 'kim',
    'Kình Dương': 'kim', 'Đà La': 'kim',
    'Linh Tinh': 'kim', 'Thiên La': 'kim', 'Địa Võng': 'kim',

    // ── Mộc — xanh lá ────────────────────────────────────────────────────────
    'Hóa Lộc': 'mộc', 'Phượng Các': 'mộc',
    'Ân Quang': 'mộc', 'Bát Tọa': 'mộc',
    'Đào Hoa': 'mộc', 'Giải Thần': 'mộc',
    'Đường Phù': 'mộc', 'Tướng Quân': 'mộc',
    'Tang Môn': 'mộc', 'Cô Thần': 'mộc', 'Quả Tú': 'mộc',

    // ── Thủy — đen ───────────────────────────────────────────────────────────
    'Văn Khúc': 'thủy', 'Hữu Bật': 'thủy',
    'Hóa Kỵ': 'thủy', 'Long Trì': 'thủy',
    'Thiên Quý': 'thủy', 'Tam Thai': 'thủy',
    'Hồng Loan': 'thủy', 'Thiên Hỷ': 'thủy',
    'Thanh Long': 'thủy', 'Long Đức': 'thủy',
    'Tràng Sinh': 'thủy', 'Mộc Dục': 'thủy',
    'Suy': 'thủy', 'Tử': 'thủy',
    'Bác Sĩ': 'thủy', 'Thiếu Âm': 'thủy',
    'Thiên Khốc': 'thủy', 'Thiên Hư': 'thủy',
    'Thiên Diêu': 'thủy', 'Thiên Y': 'thủy',
    'Lưu Hà': 'thủy', 'Thiên Sứ': 'thủy',

    // ── Hỏa — đỏ ─────────────────────────────────────────────────────────────
    'Thiên Khôi': 'hỏa', 'Thiên Việt': 'hỏa',
    'Thiên Mã': 'hỏa', 'Thiên Quan': 'hỏa',
    'Thiên Giải': 'hỏa', 'Thiên Đức': 'hỏa',
    'Nguyệt Đức': 'hỏa', 'Bệnh': 'hỏa',
    'Lực Sĩ': 'hỏa', 'Đại Hao': 'hỏa',
    'Tiểu Hao': 'hỏa', 'Phi Liêm': 'hỏa',
    'Hỷ Thần': 'hỏa', 'Thiếu Dương': 'hỏa',
    'Quan Phù': 'hỏa', 'Tử Phù': 'hỏa',
    'Trực Phù': 'hỏa', 'Tuế Phá': 'hỏa',
    'Điếu Khách': 'hỏa', 'Văn Tinh': 'hỏa',
    'Hỏa Tinh': 'hỏa', 'Thiên Hình': 'hỏa',
    'Thiên Không': 'hỏa', 'Địa Không': 'hỏa',
    'Địa Kiếp': 'hỏa', 'Kiếp Sát': 'hỏa',
    'Đẩu Quân': 'hỏa', 'Phá Toái': 'hỏa',

    // ── Thổ — vàng ───────────────────────────────────────────────────────────
    'Tả Phụ': 'thổ', 'Lộc Tồn': 'thổ',
    'Hóa Quyền': 'thổ', 'Phong Cáo': 'thổ',
    'Thiên Phúc': 'thổ', 'Địa Giải': 'thổ',
    'Phúc Đức': 'thổ', 'Thiên Thọ': 'thổ',
    'Thiên Tài': 'thổ', 'Thiên Trù': 'thổ',
    'Quốc Ấn': 'thổ', 'Mộ': 'thổ',
    'Thai': 'thổ', 'Dưỡng': 'thổ',
    'Bệnh Phù': 'thổ', 'Phục Binh': 'thổ',
    'Quan Phủ': 'thổ', 'Thái Tuế': 'thổ',
    'Thiên Thương': 'thổ',
    // Giữ lại các sao không trong danh sách
    'Tai Sát': 'thổ', 'Thiên Sát': 'thổ',
    'Nguyệt Sát': 'thổ', 'Vong Thần': 'thổ',
    'Tuần Không': 'hỏa', 'Triệt Lộ': 'kim',
};

// Trạng thái sáng tối của sao phụ tinh tại từng cung (Đắc/Hãm)
// Miếu + Vượng + Đắc → (Đ)   |   Hãm → (H)   |   Còn lại → không ghi
const SECONDARY_BRIGHTNESS = {
    'Văn Xương': {
        dac: new Set(['Tỵ','Dậu','Sửu','Thân','Tý','Thìn','Hợi']),
        ham: new Set(['Dần','Ngọ','Tuất']),
    },
    'Văn Khúc': {
        dac: new Set(['Tỵ','Sửu','Dậu','Hợi','Mão','Mùi','Thân','Tý','Thìn']),
        ham: new Set(['Ngọ','Tuất']),
    },
    'Tả Phụ':    { dac: new Set(['Thìn','Tuất','Sửu','Mùi']) },
    'Hữu Bật':   { dac: new Set(['Thìn','Tuất','Sửu','Mùi']) },
    'Thiên Mã':  { dac: new Set(['Tỵ','Dần']) },
    'Kình Dương':{ dac: new Set(['Thìn','Tuất','Sửu','Mùi']), ham: new Set(['Tý','Ngọ','Mão','Dậu']) },
    'Đà La':     { dac: new Set(['Thìn','Tuất','Sửu','Mùi']), ham: new Set(['Dần','Thân','Tỵ','Hợi']) },
    'Hỏa Tinh':  { dac: new Set(['Dần','Ngọ','Tuất','Tỵ','Dậu','Sửu','Hợi','Mão','Mùi']), ham: new Set(['Thân','Tý','Thìn']) },
    'Linh Tinh': { dac: new Set(['Dần','Tuất','Thìn','Tỵ','Mùi']), ham: new Set(['Dậu','Sửu','Hợi']) },
    'Đại Hao':   { dac: new Set(['Dần','Thân','Mão','Dậu']), ham: new Set(['Tý','Ngọ','Tỵ','Hợi']) },
    'Tiểu Hao':  { dac: new Set(['Dần','Thân','Mão','Dậu']), ham: new Set(['Tý','Ngọ','Tỵ','Hợi']) },
    'Tang Môn':  { dac: new Set(['Dần','Thân','Mão','Dậu']) },
    'Bạch Hổ':   { dac: new Set(['Dần','Thân','Mão','Dậu']) },
    'Thiên Khốc':{ dac: new Set(['Tý','Ngọ','Mão','Dậu','Sửu','Mùi']) },
    'Thiên Hư':  { dac: new Set(['Tý','Ngọ','Mão','Dậu','Sửu','Mùi']) },
    'Thiên Hình':{ dac: new Set(['Dần','Thân','Mão','Dậu']) },
    'Địa Không': { dac: new Set(['Tỵ','Hợi','Dần','Thân']) },
    'Địa Kiếp':  { dac: new Set(['Tỵ','Hợi','Dần','Thân']) },
    'Thiên Diêu':{ dac: new Set(['Dần','Mão','Dậu','Tuất']) },
};

function getSecondaryBrightness(starName, diaChi) {
    const info = SECONDARY_BRIGHTNESS[starName];
    if (!info) return '';
    if (info.dac && info.dac.has(diaChi)) return '(Đ)';
    if (info.ham && info.ham.has(diaChi)) return '(H)';
    return '';
}

// Can → element & sign for đại vận footer
const CAN_ELEMENT_VN = {
    'Giáp':'MỘC','Ất':'MỘC','Bính':'HỎA','Đinh':'HỎA',
    'Mậu':'THỔ','Kỷ':'THỔ','Canh':'KIM','Tân':'KIM',
    'Nhâm':'THỦY','Quý':'THỦY'
};
const DUONG_CAN_SET = new Set(['Giáp','Bính','Mậu','Canh','Nhâm']);

function abbrevCanChi(canChi) {
    if (!canChi) return '';
    const parts = canChi.trim().split(' ');
    return parts.length >= 2 ? parts[0][0] + '. ' + parts[1] : canChi;
}

function getDaiHanElem(daiHan) {
    if (!daiHan?.can_chi) return '';
    const can = daiHan.can_chi.trim().split(' ')[0];
    const elem = CAN_ELEMENT_VN[can] || '';
    if (!elem) return '';
    return (DUONG_CAN_SET.has(can) ? '+' : '−') + elem;
}

const CHI_ELEMENT_MAP = {
    'Tý':  { elem: 'THỦY', duong: true  },
    'Sửu': { elem: 'THỔ',  duong: false },
    'Dần': { elem: 'MỘC',  duong: true  },
    'Mão': { elem: 'MỘC',  duong: false },
    'Thìn':{ elem: 'THỔ',  duong: true  },
    'Tỵ':  { elem: 'HỎA',  duong: false },
    'Ngọ': { elem: 'HỎA',  duong: true  },
    'Mùi': { elem: 'THỔ',  duong: false },
    'Thân':{ elem: 'KIM',  duong: true  },
    'Dậu': { elem: 'KIM',  duong: false },
    'Tuất':{ elem: 'THỔ',  duong: true  },
    'Hợi': { elem: 'THỦY', duong: false },
};

function getDiaChiElem(diaChi) {
    const info = CHI_ELEMENT_MAP[diaChi];
    if (!info) return '';
    return (info.duong ? '+' : '−') + info.elem;
}

function getBrightnessParens(brightness) {
    if (!brightness) return '';
    const b = brightness.toLowerCase();
    if (b.includes('miếu') || b.includes('mieu')) return '(M)';
    if (b.includes('vượng') || b.includes('vuong')) return '(V)';
    if (b.includes('đắc') || b.includes('dac')) return '(Đ)';
    if (b.includes('bình') || b.includes('binh')) return '(B)';
    if (b.includes('hãm') || b.includes('ham')) return '(H)';
    return '';
}

const STAR_MEANINGS = {
    'Tử Vi': 'Ngôi sao quan trọng nhất, đại diện cho quyền uy và may mắn.',
    'Thiên Phủ': 'Sao của quyền lực và che chở, mang lại cơ hội lãnh đạo.',
    'Thái Dương': 'Sao của danh tiếng và sự nghiệp, mang ánh sáng và thành công.',
    'Thái Âm': 'Sao của nghệ thuật và tình cảm, mang lại sự mềm mại.',
    'Liêm Trinh': 'Sao của sự thông minh và công việc, mang lại trí tuệ.',
    'Tham Lang': 'Sao của sự nghiệp và tham vọng, mang lại động lực.',
    'Cự Môn': 'Sao của sự thay đổi và thử thách, mang lại sự trưởng thành.',
    'Thiên Tướng': 'Sao của quân sự và lãnh đạo, mang lại quyền lực.',
    'Vũ Khúc': 'Sao của tài lộc và may mắn, mang lại của cải.',
    'Thiên Đồng': 'Sao của sự phát triển và học tập, mang lại trí tuệ.',
    'Thiên Cơ': 'Sao của sự sáng tạo và kỹ thuật, mang lại tài năng.',
    'Thiên Lương': 'Sao của sự trung thành và hỗ trợ, mang lại quý nhân.',
    'Thất Sát': 'Sao của sự nghiêm nghị và kỷ luật, mang lại quyền lực.',
    'Phá Quân': 'Sao của sự phá vỡ và thay đổi, mang lại cơ hội mới.'
};

let currentChartData = null;
let currentTuviData = null;

// TVF-4: Advanced view state — always read from localStorage for accuracy
function isAdvancedView() {
    return localStorage.getItem('tuvi_advanced_view') === 'true';
}

function toggleAdvancedView() {
    const next = !isAdvancedView();
    localStorage.setItem('tuvi_advanced_view', String(next));
    if (currentTuviData) renderChart(currentTuviData);

    const btn = document.getElementById('btn-advanced-toggle');
    if (btn) btn.textContent = isAdvancedView() ? '📋 Xem Cơ Bản' : '🔍 Xem Chuyên Sâu';
}

// =========================================
// TVF-5: Per-Palace Interpretation
// =========================================
const PALACE_DOMAINS = {
    'Mệnh':      'vận mệnh tổng quát, tính cách, xu hướng cuộc đời',
    'Phu Thê':   'tình duyên, hôn nhân, mối quan hệ tình cảm',
    'Quan Lộc':  'sự nghiệp, công danh, phát triển nghề nghiệp',
    'Tài Bạch':  'tài chính, tiền bạc, nguồn thu nhập',
    'Tật Ách':   'sức khỏe, thể chất, những bệnh tật cần lưu ý',
    'Tử Tức':    'con cái, hậu duệ, mối quan hệ với thế hệ sau',
    'Huynh Đệ':  'anh chị em, bạn bè thân, đồng nghiệp',
    'Điền Trạch':'nhà cửa, bất động sản, tài sản cố định',
    'Phúc Đức':  'phúc đức, đời sống tinh thần, tâm linh',
    'Phụ Mẫu':   'cha mẹ, gia đình, sự hỗ trợ từ bề trên',
    'Thiên Di':  'di chuyển, du lịch, quan hệ xã hội bên ngoài',
    'Nô Bộc':    'thuộc hạ, nhân viên, người giúp đỡ xung quanh',
};

function getPalaceDomain(cungName) {
    return PALACE_DOMAINS[cungName] || cungName;
}

// TPD-2: Domain-specific button labels for all 12 palaces
const PALACE_BUTTON_LABELS = {
    'Mệnh':      'Luận Giải Mệnh',
    'Phu Thê':   'Luận Giải Tình Duyên',
    'Quan Lộc':  'Luận Giải Sự Nghiệp',
    'Tài Bạch':  'Luận Giải Tài Lộc',
    'Tật Ách':   'Luận Giải Sức Khỏe',
    'Tử Tức':    'Luận Giải Con Cái',
    'Huynh Đệ':  'Luận Giải Huynh Đệ',
    'Điền Trạch':'Luận Giải Nhà Cửa',
    'Phúc Đức':  'Luận Giải Phúc Đức',
    'Phụ Mẫu':   'Luận Giải Phụ Mẫu',
    'Thiên Di':  'Luận Giải Xuất Hành',
    'Nô Bộc':    'Luận Giải Giao Tế',
};

function getPalaceButtonLabel(cungName) {
    return PALACE_BUTTON_LABELS[cungName] || 'Luận Giải Cung Này';
}

// Tam hợp groups (positions 1-12): [1,5,9], [2,6,10], [3,7,11], [4,8,12]
function getTamHopPositions(position) {
    const groups = [[1,5,9],[2,6,10],[3,7,11],[4,8,12]];
    for (const group of groups) {
        if (group.includes(position)) return group.filter(p => p !== position);
    }
    return [];
}

async function interpretPalace(palacePosition) {
    if (!currentTuviData) return;

    const palace = (currentTuviData.palaces || []).find(p => p.position === palacePosition);
    if (!palace) return;

    // Freemium gate
    const usageCheck = await checkServerUsage('tuvi', API_BASE);
    if (!usageCheck.allowed) {
        if (typeof showPaywallModal === 'function') showPaywallModal('tuvi');
        return;
    }

    // Get content element (desktop side panel or mobile bottom sheet)
    const isMobile = typeof window !== 'undefined' && window.innerWidth <= 600;
    const contentEl = isMobile
        ? document.getElementById('bottom-sheet-content')
        : document.getElementById('detail-content');
    if (!contentEl) return;

    // Show loading
    const domain = getPalaceDomain(palace.cung_name);
    contentEl.innerHTML = `<div class="ai-loading-text">Đang luận giải cung ${palace.cung_name}...</div>`;

    // Build focused chart data (target + tam hợp + Mệnh)
    const tamHopPositions = getTamHopPositions(palace.position);
    const focusedPalaces = [palace];
    for (const pos of tamHopPositions) {
        const p = (currentTuviData.palaces || []).find(x => x.position === pos);
        if (p) focusedPalaces.push(p);
    }
    const menhPalace = (currentTuviData.palaces || []).find(x => x.cung_name === 'Mệnh');
    if (menhPalace && menhPalace.position !== palace.position) focusedPalaces.push(menhPalace);

    const focusedChartData = {
        palaces: focusedPalaces,
        nap_am:   currentTuviData.nap_am,
        cuc:      currentTuviData.cuc,
        menh_chu: currentTuviData.menh_chu,
        than_chu: currentTuviData.than_chu,
        tu_hoa:   currentTuviData.tu_hoa,
    };

    const focusedQuestion = `Luận giải chuyên sâu cung ${palace.cung_name} về ${domain}`;
    const deviceId = getDeviceId('tuvi_device_id');

    try {
        const response = await fetch(`${API_BASE}/api/tuvi/interpret/palace?device_id=${encodeURIComponent(deviceId)}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question:              focusedQuestion,
                birth_info:            currentTuviData.birth ? currentTuviData.birth.solar : {},
                chart_data:            focusedChartData,
                static_interpretation: palace.meaning || '',
            }),
        });

        if (!response.ok) throw new Error('Interpretation failed');

        contentEl.innerHTML = '';
        let usageIncremented = false;
        await readSSEStream(response, contentEl, {
            appName: 'tuvi',
            readingId: 'palace_' + palacePosition + '_' + Date.now().toString(36),
            onDone: async () => {
                if (!usageIncremented) {
                    usageIncremented = true;
                    await incrementServerUsage('tuvi', API_BASE);
                }
                // Add "Xem lại" restore button
                const backBtn = document.createElement('button');
                backBtn.className = 'btn-back-palace';
                backBtn.textContent = '← Xem lại thông tin cung';
                backBtn.onclick = () => { contentEl.innerHTML = buildDetailHTML(palace); };
                contentEl.appendChild(backBtn);
            },
        });
    } catch (e) {
        console.error('Palace interpretation error:', e);
        contentEl.innerHTML = `<p style="color:var(--error);">Lỗi: ${e.message}</p>`;
        const backBtn = document.createElement('button');
        backBtn.className = 'btn-back-palace';
        backBtn.textContent = '← Xem lại thông tin cung';
        backBtn.onclick = () => { contentEl.innerHTML = buildDetailHTML(palace); };
        contentEl.appendChild(backBtn);
    }
}

function getElementClass(element) {
    const map = {
        'kim': 'kim', 'mộc': 'moc', 'moc': 'moc',
        'thủy': 'thuy', 'thuy': 'thuy',
        'hỏa': 'hoa', 'hoa': 'hoa',
        'thổ': 'tho', 'tho': 'tho'
    };
    return map[element?.toLowerCase()] || '';
}

// Triệt Lộ / Tuần Không — special badge styling
function getSpecialStarClass(name) {
    if (name === 'Triệt Lộ') return 'star-triet-lo';
    if (name === 'Tuần Không') return 'star-tuan-khong';
    return '';
}

function getElementColor(element) {
    const map = {
        'kim': 'var(--kim)', 'mộc': 'var(--moc)', 'moc': 'var(--moc)',
        'thủy': 'var(--thuy)', 'thuy': 'var(--thuy)',
        'hỏa': 'var(--hoa)', 'hoa': 'var(--hoa)',
        'thổ': 'var(--tho)', 'tho': 'var(--tho)'
    };
    return map[element?.toLowerCase()] || 'var(--text-secondary)';
}

function getBrightnessClass(brightness) {
    if (!brightness) return '';
    const b = brightness.toLowerCase();
    if (b.includes('miếu') || b.includes('mieu')) return 'mieu';
    if (b.includes('vượng') || b.includes('vuong')) return 'vuong';
    if (b.includes('đắc') || b.includes('dac')) return 'dac';
    if (b.includes('bình') || b.includes('binh')) return 'binh';
    if (b.includes('hãm') || b.includes('ham')) return 'ham';
    return '';
}

function getBrightnessLabel(brightness) {
    if (!brightness) return '';
    const b = brightness.toLowerCase();
    if (b.includes('miếu') || b.includes('mieu')) return 'M';
    if (b.includes('vượng') || b.includes('vuong')) return 'V';
    if (b.includes('đắc') || b.includes('dac')) return 'Đ';
    if (b.includes('bình') || b.includes('binh')) return 'B';
    if (b.includes('hãm') || b.includes('ham')) return 'H';
    return '';
}

function getTuHoaClass(tuHoa) {
    if (!tuHoa) return '';
    const t = tuHoa.toLowerCase();
    if (t.includes('lộc') || t.includes('loc')) return 'loc';
    if (t.includes('quyền') || t.includes('quyen')) return 'quyen';
    if (t.includes('khoa')) return 'khoa';
    if (t.includes('kỵ') || t.includes('ky')) return 'ky';
    return '';
}

// =========================================
// TVF-2: CENTER PANEL HTML BUILDER
// =========================================
const _DUONG_CAN = new Set(['Giáp', 'Bính', 'Mậu', 'Canh', 'Nhâm']);

function buildCenterPanelHTML(data) {
    const solar    = data.birth?.solar  || {};
    const lunar    = data.birth?.lunar  || {};
    const napAm    = data.nap_am?.name  || data.nap_am?.ngu_hanh || '';
    const cuc      = data.cuc?.name     || '';
    const menhChu  = data.menh_chu          || '';
    const thanChu  = data.than_chu          || '';
    const canLuong = data.can_luong?.display || '';
    const tuHoa    = data.tu_hoa            || null;
    const menhQuai = data.cung_menh     || '?';
    const thanQuai = data.cung_than     || '?';

    // Âm/Dương Nam/Nữ — dựa vào can năm và giới tính
    const yearCanChi = data.birth?.can_chi?.year || '';
    const yearCan    = yearCanChi.split(' ')[0] || '';
    const isDuong    = _DUONG_CAN.has(yearCan);
    const isNam      = (data.gender || '').toLowerCase().includes('nam') || (data.gender || '').toLowerCase() === 'm' || (data.gender || '').toLowerCase() === 'male';
    const amDuongLabel = `${isDuong ? 'DƯƠNG' : 'ÂM'} ${isNam ? 'NAM' : 'NỮ'}`;

    const TU_HOA_LABELS = [
        { key: 'hoa_lộc',   label: 'Lộc',    dot: 'loc'   },
        { key: 'hoa_quyền', label: 'Quyền',  dot: 'quyen' },
        { key: 'hoa_khoa',  label: 'Khoa',   dot: 'khoa'  },
        { key: 'hoa_kỵ',    label: 'Kỵ',     dot: 'ky'    },
    ];

    let tuHoaHTML = '';
    if (tuHoa) {
        const rows = TU_HOA_LABELS.map(({ key, label, dot }) => {
            const entry = tuHoa[key];
            if (!entry) return '';
            return `<div class="center-tuhua-row">
                <span class="star-tu-hoa ${dot}"></span>
                <span class="center-tuhua-label">${label}:</span>
                <span class="center-tuhua-value">${entry.star || ''}</span>
            </div>`;
        }).join('');
        if (rows.trim()) {
            tuHoaHTML = `
                <div class="center-section-label">── Tứ Hóa ──</div>
                <div class="center-tuhua">${rows}</div>`;
        }
    }

    return `
        <div class="center-title">Tử Vi Lá Số</div>
        <div class="center-birth">
            <div>Dương: ${solar.day || '?'}/${solar.month || '?'}/${solar.year || '?'}</div>
            <div>Âm: ${lunar.day || '?'}/${lunar.month || '?'}/${lunar.year || '?'}</div>
            ${napAm    ? `<div>Nạp Âm: ${napAm}</div>`      : ''}
            ${cuc      ? `<div>Cục: ${cuc}</div>`            : ''}
            ${menhChu  ? `<div>Mệnh Chủ: ${menhChu}</div>`  : ''}
            ${thanChu  ? `<div>Thân Chủ: ${thanChu}</div>`  : ''}
            ${amDuongLabel ? `<div class="center-am-duong">${amDuongLabel}</div>` : ''}
        </div>
        ${canLuong ? `<div class="center-can-luong">⚖ ${canLuong}</div>` : ''}
        <div class="center-badges">
            ${menhQuai ? `<span class="center-badge">命 ${menhQuai}</span>` : ''}
            ${thanQuai ? `<span class="center-badge">身 ${thanQuai}</span>` : ''}
        </div>
        ${tuHoaHTML}
        <div class="brightness-legend">
            <div class="brightness-legend-title">── Cường Độ Sao ──</div>
            <div class="brightness-legend-items">
                <span class="brightness-legend-item brightness-mieu">Miếu (M) — Cực vượng</span>
                <span class="brightness-legend-item brightness-vuong">Vượng (V) — Sao mạnh</span>
                <span class="brightness-legend-item brightness-dac">Đắc (Đ) — Khá tốt</span>
                <span class="brightness-legend-item brightness-binh">Bình (B) — Trung tính</span>
                <span class="brightness-legend-item brightness-ham">Hãm (H) — Sao yếu</span>
            </div>
        </div>
    `;
}

// =========================================
// RENDER CHART — R2
// =========================================
function renderChart(data) {
    currentChartData = data;
    currentTuviData = data;

    const aiSection = document.getElementById('ai-section');
    if (aiSection) aiSection.classList.remove('hidden');

    // Hiện section Luận Giải
    const lgSection = document.getElementById('lg-section');
    if (lgSection) lgSection.classList.remove('hidden');

    showLuuNienButton();
    showCompatibilityButton();

    const container = document.getElementById('chart-container');
    if (!container) return;
    container.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'chart-grid-wrapper';

    const grid = document.createElement('div');
    grid.className = 'chart-grid';

    const menhDiaChi = data.cung_menh || '';
    const thanDiaChi = data.cung_than || '';

    // Build palace elements
    const palaceElements = {};

    for (let pos = 1; pos <= 12; pos++) {
        const palace = data.palaces?.find(p => p.position === pos);
        if (!palace) continue;

        const el = document.createElement('div');
        el.className = 'palace palace-enter';
        el.setAttribute('role', 'button');
        el.setAttribute('tabindex', '0');
        const cungName = palace.cung_name || '';
        el.setAttribute('aria-label', `${palace.dia_chi} - ${cungName}`);

        const isMenh = palace.dia_chi === menhDiaChi;
        // Thân luôn đồng cung — không loại trừ trường hợp đồng cung Mệnh
        const isThan = palace.dia_chi === thanDiaChi;
        if (isMenh) el.classList.add('menh');
        if (isThan && !isMenh) el.classList.add('than');
        if (isMenh && isThan) el.classList.add('menh-than');

        el.onclick = () => openDetailPanel(palace);
        el.onkeydown = (e) => { if (e.key === 'Enter' || e.key === ' ') openDetailPanel(palace); };

        // TVF-1: Hover popup (desktop only)
        let hoverTimer = null;
        el.addEventListener('mouseenter', () => {
            hoverTimer = setTimeout(() => openDetailPanel(palace), 300);
        });
        el.addEventListener('mouseleave', () => {
            clearTimeout(hoverTimer);
        });

        // Watermark: Mệnh+Thân đồng cung → chỉ icon 命 (header đã ghi <THÂN>)
        if (isMenh || isThan) {
            const wm = document.createElement('span');
            wm.className = 'palace-watermark';
            wm.textContent = isMenh ? '命' : '身';
            el.appendChild(wm);
        }

        // ── HEADER: [can_chi_abbr] [CUNG NAME [<THÂN>]] [đại vận start age] ──
        const dh = palace.dai_han;
        const dhAge = dh?.range?.[0] ?? '';
        const canAbbr = abbrevCanChi(palace.can_chi);
        const thanTag = isThan ? ' <span class="palace-than-tag">&lt;THÂN&gt;</span>' : '';
        const header = document.createElement('div');
        header.className = 'palace-header';
        header.innerHTML = `
            <span class="palace-can-abbr">${canAbbr}</span>
            <span class="palace-cung">${cungName}${thanTag}</span>
            <span class="palace-dh-age">${dhAge}</span>
        `;
        el.appendChild(header);

        // ── CHÍNH TINH (bold, centered, brightness in parens) ──
        const stars = palace.stars || [];
        const mainStars = stars.filter(s => MAIN_STARS.has(s.name));
        if (mainStars.length > 0) {
            const mainDiv = document.createElement('div');
            mainDiv.className = 'palace-main-stars';
            mainStars.forEach(star => {
                const starEl = document.createElement('span');
                starEl.className = 'star-main';
                const color = getElementColor(star.element);
                const bp = getBrightnessParens(star.brightness);
                const bClass = getBrightnessClass(star.brightness);
                const thClass = getTuHoaClass(star.tu_hoa);
                let html = `<span style="color:${color};">${star.name.toUpperCase()}</span>`;
                if (bp) html += ` <span class="star-brightness-parens ${bClass}">${bp}</span>`;
                if (thClass) html += `<span class="star-tu-hoa ${thClass}"></span>`;
                starEl.innerHTML = html;
                mainDiv.appendChild(starEl);
            });
            el.appendChild(mainDiv);
        }

        // ── BODY: hai cột — sao tốt trái, sao xấu phải ──
        // Gộp tất cả: phụ tinh + tạp tinh + tứ hóa (hiển thị trực tiếp)
        const auxRaw = stars.filter(s => !MAIN_STARS.has(s.name));
        const adjRaw = palace.adjective_stars || [];
        // Tứ hóa từ chính tinh → thêm làm sao độc lập
        const tuHoaStars = stars
            .filter(s => s.tu_hoa)
            .map(s => ({ name: s.tu_hoa, element: null, brightness: null, tu_hoa: null }));
        const allSecondary = [
            ...auxRaw.map(s => ({ name: s.name, element: s.element, brightness: s.brightness, tu_hoa: null })),
            ...adjRaw.map(s => ({ name: s.name, element: null, brightness: s.brightness, tu_hoa: null })),
            ...tuHoaStars,
        ];
        // Loại trùng (cùng tên)
        const seen = new Set();
        const allSecondaryUniq = allSecondary.filter(s => seen.has(s.name) ? false : seen.add(s.name));
        const goodStars = allSecondaryUniq.filter(s => !BAD_STARS.has(s.name));
        const SPECIAL_LAST = new Set(['Tuần Không', 'Triệt Lộ']);
        const badStars  = [
            ...allSecondaryUniq.filter(s =>  BAD_STARS.has(s.name) && !SPECIAL_LAST.has(s.name)),
            ...allSecondaryUniq.filter(s =>  BAD_STARS.has(s.name) &&  SPECIAL_LAST.has(s.name)),
        ];

        const bodyDiv = document.createElement('div');
        bodyDiv.className = 'palace-body';

        const goodCol = document.createElement('div');
        goodCol.className = 'palace-col-good';
        goodStars.forEach(star => {
            const span = document.createElement('span');
            const specialClass = getSpecialStarClass(star.name);
            span.className = 'star-aux' + (specialClass ? ' ' + specialClass : '');
            if (!specialClass) {
                const elemColor = getElementColor(star.element || STAR_ELEMENT_MAP[star.name]);
                span.style.color = elemColor;
            }
            const sb = getSecondaryBrightness(star.name, palace.dia_chi);
            span.textContent = sb ? `${star.name} ${sb}` : star.name;
            goodCol.appendChild(span);
        });

        const badCol = document.createElement('div');
        badCol.className = 'palace-col-bad';
        badStars.forEach(star => {
            const span = document.createElement('span');
            const specialClass = getSpecialStarClass(star.name);
            span.className = 'star-aux star-aux-bad' + (specialClass ? ' ' + specialClass : '');
            if (!specialClass) {
                const elemColor = getElementColor(star.element || STAR_ELEMENT_MAP[star.name]);
                span.style.color = elemColor;
            }
            const sb = getSecondaryBrightness(star.name, palace.dia_chi);
            span.textContent = sb ? `${star.name} ${sb}` : star.name;
            badCol.appendChild(span);
        });

        bodyDiv.appendChild(goodCol);
        bodyDiv.appendChild(badCol);
        el.appendChild(bodyDiv);

        // ── SẮO LƯU NĂM ──
        const luuStars = palace.luu_stars || [];
        if (luuStars.length > 0) {
            const luuDiv = document.createElement('div');
            luuDiv.className = 'palace-luu-stars';
            luuStars.forEach(name => {
                const span = document.createElement('span');
                span.className = 'star-luu';
                const baseName = name.replace(/^L\. /, '');
                const elemColor = getElementColor(STAR_ELEMENT_MAP[baseName] || STAR_ELEMENT_MAP[name]);
                span.style.color = elemColor;
                span.textContent = name;
                luuDiv.appendChild(span);
            });
            el.appendChild(luuDiv);
        }

        // ── FOOTER: [tràng sinh] bên trái | [đại vận element] bên phải ──
        const footer = document.createElement('div');
        footer.className = 'palace-footer';
        const tsVal = palace.trang_sinh || '';
        const tsColor = tsVal ? getElementColor(STAR_ELEMENT_MAP[tsVal]) : 'var(--text-muted)';
        const chiElem = getDiaChiElem(palace.dia_chi);
        const chiInfo = CHI_ELEMENT_MAP[palace.dia_chi];
        const chiElemColor = chiInfo ? getElementColor(chiInfo.elem.toLowerCase()) : 'var(--text-secondary)';
        footer.innerHTML = `
            <span class="palace-ts" style="color:${tsColor}">${tsVal}</span>
            <span class="palace-dh-elem" style="color:${chiElemColor}">${chiElem}</span>
        `;
        el.appendChild(footer);

        // Mobile star dots
        if (stars.length > 0) {
            const dotsDiv = document.createElement('div');
            dotsDiv.className = 'palace-star-dots';
            stars.forEach(() => {
                const dot = document.createElement('span');
                dot.className = 'palace-star-dot';
                dotsDiv.appendChild(dot);
            });
            el.appendChild(dotsDiv);
        }

        palaceElements[pos] = el;
    }

    // Place palaces with staggered animation
    CLOCKWISE_ORDER.forEach((pos, idx) => {
        if (!palaceElements[pos]) return;
        const placement = PALACE_GRID[pos];
        if (placement) {
            palaceElements[pos].style.gridRow    = placement.row;
            palaceElements[pos].style.gridColumn = placement.col;
            palaceElements[pos].style.animationDelay = `${idx * 60}ms`;
        }
        grid.appendChild(palaceElements[pos]);
    });

    // TVF-2: Center panel with enhanced content
    const centerPanel = document.createElement('div');
    centerPanel.className = 'center-panel palace-enter';
    centerPanel.style.gridRow    = '2 / 4';
    centerPanel.style.gridColumn = '2 / 4';
    // Center panel fades in after all 12 palaces (12 × 60ms + 400ms)
    centerPanel.style.animationDelay = `${CLOCKWISE_ORDER.length * 60 + 400}ms`;
    centerPanel.innerHTML = buildCenterPanelHTML(data);

    grid.appendChild(centerPanel);
    wrapper.appendChild(grid);

    // TVF-4: Advanced toggle button below chart
    const toggleBtn = document.createElement('button');
    toggleBtn.id = 'btn-advanced-toggle';
    toggleBtn.className = 'btn-advanced-toggle';
    toggleBtn.textContent = isAdvancedView() ? '📋 Xem Cơ Bản' : '🔍 Xem Chuyên Sâu';
    toggleBtn.onclick = toggleAdvancedView;
    wrapper.appendChild(toggleBtn);

    container.appendChild(wrapper);

    renderTimeline(data);

    // Collapse form after successful render
    collapseForm();

    // TV-FP-2: show share button
    const shareSection = document.getElementById('share-section');
    if (shareSection) shareSection.classList.remove('hidden');

    // TV-FP-4: save to history sidebar
    const params = {
        day:    parseInt(document.getElementById('day')?.value),
        month:  parseInt(document.getElementById('month')?.value),
        year:   parseInt(document.getElementById('year')?.value),
        hour:   parseInt(document.getElementById('hour')?.value) || 0,
        minute: parseInt(document.getElementById('minute')?.value) || 0,
        gender: document.querySelector('input[name="gender"]:checked')?.value || 'nam'
    };
    if (typeof saveTuviHistory === 'function') {
        const entry = saveTuviHistory(params, data);
        if (entry && entry.id) updateOgMeta(entry.id);
    }

    // TV-FP-3: show push opt-in after first chart (never on page load)
    if (typeof showPushOptIn === 'function') showPushOptIn();
}

// =========================================
// RENDER TIMELINE — R4
// =========================================
function renderTimeline(data) {
    const timelineSection   = document.getElementById('timeline-section');
    const timelineContainer = document.getElementById('timeline');
    const summarydiv        = document.getElementById('timeline-summary');

    if (!timelineSection || !timelineContainer) return;

    timelineContainer.innerHTML = '';
    if (summarydiv) summarydiv.classList.add('hidden');

    const daiHan         = data.dai_han         || [];
    const tieuHan        = data.tieu_han        || null;
    const tieuHanUpcoming = data.tieu_han_upcoming || [];
    const birthYear      = data.birth?.solar?.year || data.birth?.lunar?.year || 1990;
    const currentYear    = new Date().getFullYear();
    const currentAge     = currentYear - birthYear;

    let timelineData = daiHan.map(dh => ({
        age:          `${dh.start_age}–${dh.end_age}`,
        start:        dh.start_age,
        end:          dh.end_age,
        can_chi:      dh.period || '',
        palace:       dh.palace_name || '',
        palace_index: dh.palace_index,
        is_current:   currentAge >= dh.start_age && currentAge <= dh.end_age,
        is_tieu_han:  tieuHan && tieuHan.palace_index === dh.palace_index
    }));

    timelineData.sort((a, b) => a.start - b.start);

    if (timelineData.length === 0) {
        const fallback = [
            { age: '0–10',   start: 0,  end: 10,  palace: 'Mệnh',     can_chi: 'Dần' },
            { age: '10–20',  start: 10, end: 20,  palace: 'Phụ Mẫu',  can_chi: 'Mão' },
            { age: '20–30',  start: 20, end: 30,  palace: 'Điền Trạch',can_chi: 'Thìn' },
            { age: '30–40',  start: 30, end: 40,  palace: 'Quan Lộc',  can_chi: 'Tỵ' },
            { age: '40–50',  start: 40, end: 50,  palace: 'Tài Bạch',  can_chi: 'Ngọ' },
            { age: '50–60',  start: 50, end: 60,  palace: '',          can_chi: 'Mùi' },
            { age: '60–70',  start: 60, end: 70,  palace: '',          can_chi: 'Thân' },
            { age: '70–80',  start: 70, end: 80,  palace: '',          can_chi: 'Dậu' },
            { age: '80–90',  start: 80, end: 90,  palace: '',          can_chi: 'Tuất' },
            { age: '90–100', start: 90, end: 100, palace: '',          can_chi: 'Hợi' }
        ];
        timelineData = fallback.map(s => ({ ...s, is_current: currentAge >= s.start && currentAge < s.end, is_tieu_han: false }));
    }

    let currentEl = null;

    timelineData.forEach(segment => {
        const el = document.createElement('div');
        el.className = 'timeline-segment';

        if (segment.is_current) {
            el.classList.add('current');
            currentEl = el;
        } else if (segment.start > currentAge) {
            el.classList.add('future');
        }
        if (segment.is_tieu_han) el.classList.add('tieu-han');

        const chi = segment.can_chi || '';
        const palace = segment.palace ? `\n${segment.palace}` : '';

        el.innerHTML = `<span class="age">${segment.age}</span><span class="chi">${chi}${palace}</span>`;

        if (segment.is_current || segment.is_tieu_han) {
            let t = [];
            if (segment.is_current) t.push('Đại Hạn hiện tại');
            if (segment.is_tieu_han) t.push('Tiểu Hạn');
            el.title = t.join(' + ');
        }

        timelineContainer.appendChild(el);
    });

    // Auto-scroll to current period
    if (currentEl) {
        setTimeout(() => {
            currentEl.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
        }, 800);
    }

    // Summary banner
    if (summarydiv) {
        const curr = timelineData.find(t => t.is_current);
        let summaryText = '';
        if (curr) summaryText += `🔮 Đại Hạn: ${curr.palace || curr.can_chi} (${curr.age} tuổi)`;
        if (tieuHan) summaryText += (summaryText ? ' · ' : '') + `✨ Tiểu Hạn: ${tieuHan.palace_name || ''} (năm ${tieuHan.year || ''})`;
        if (tieuHanUpcoming && tieuHanUpcoming.length) {
            summaryText += `<br><small>Tiểu Hạn sắp tới: ${tieuHanUpcoming.map(t => t.palace_name).join(', ')}</small>`;
        }
        if (summaryText) {
            summarydiv.innerHTML = summaryText;
            summarydiv.classList.remove('hidden');
        }
    }

    timelineSection.classList.remove('hidden');
    timelineSection.style.display = 'block';
}

// =========================================
// DETAIL PANEL — R5
// =========================================
function buildDetailHTML(palace) {
    const pos      = palace.position;
    const cungName = palace.cung_name || '';
    const meaning  = palace.meaning || '';
    const canChi   = palace.can_chi || '';
    const stars    = palace.stars || [];
    const mainStars = stars.filter(s => MAIN_STARS.has(s.name));
    const auxRaw2   = stars.filter(s => !MAIN_STARS.has(s.name));
    const adjRaw2   = palace.adjective_stars || [];
    const tuHoaStars2 = stars.filter(s => s.tu_hoa).map(s => ({ name: s.tu_hoa }));
    const allSecondary2 = [
        ...auxRaw2.map(s => ({ name: s.name })),
        ...adjRaw2.map(s => ({ name: s.name })),
        ...tuHoaStars2,
    ];
    const seen2 = new Set();
    const allSecondary2Uniq = allSecondary2.filter(s => seen2.has(s.name) ? false : seen2.add(s.name));
    const detailGood = allSecondary2Uniq.filter(s => !BAD_STARS.has(s.name));
    const detailBad  = allSecondary2Uniq.filter(s =>  BAD_STARS.has(s.name));
    const dh        = palace.dai_han || null;

    // TVF-1: Header with Can Chi + Đại Hạn range
    const dhRange = dh?.range ? `${dh.range[0]}–${dh.range[1]} tuổi` : '';
    const headerParts = [canChi, cungName, dhRange].filter(Boolean);

    let html = `
        <div class="detail-header">
            <h2 class="detail-title">${headerParts.join(' · ')}</h2>
            <p class="detail-subtitle">Cung thứ ${pos}</p>
        </div>
    `;

    if (meaning) {
        html += `
        <div class="detail-section">
            <h4>Ý Nghĩa Cung</h4>
            <p class="detail-interpretation">${meaning}</p>
        </div>`;
    }

    if (mainStars.length > 0) {
        html += `<div class="section-divider">Chính Tinh</div>`;
        mainStars.forEach(star => {
            const color    = getElementColor(star.element);
            const bClass   = getBrightnessClass(star.brightness);
            const thClass  = getTuHoaClass(star.tu_hoa);
            const starMeaning = STAR_MEANINGS[star.name] || '';

            let badges = '';
            if (star.brightness) badges += `<span class="star-card-badge brightness-${bClass}">${star.brightness}</span>`;
            if (star.tu_hoa)     badges += `<span class="star-card-badge tuHoa-${thClass}">${star.tu_hoa}</span>`;

            html += `
                <div class="star-card">
                    <div class="star-card-name" style="color:${color};">${star.name}</div>
                    ${badges ? `<div class="star-card-badges">${badges}</div>` : ''}
                    ${star.brightness_effect ? `<div class="star-brightness-effect">${star.brightness_effect}</div>` : ''}
                    ${starMeaning ? `<div class="star-card-meaning">${starMeaning}</div>` : ''}
                </div>
            `;
        });
    }

    if (detailGood.length > 0) {
        html += `<div class="section-divider">Sao Tốt</div>
            <div class="aux-chips-wrap">
                ${detailGood.map(s => {
                    const sc = getSpecialStarClass(s.name);
                    const sb = getSecondaryBrightness(s.name, palace.dia_chi);
                    const label = sb ? `${s.name} ${sb}` : s.name;
                    return sc
                        ? `<span class="aux-chip ${sc}">${label}</span>`
                        : `<span class="aux-chip" style="color:${getElementColor(STAR_ELEMENT_MAP[s.name])}">${label}</span>`;
                }).join('')}
            </div>`;
    }

    if (detailBad.length > 0) {
        html += `<div class="section-divider">Sao Xấu</div>
            <div class="aux-chips-wrap">
                ${detailBad.map(s => {
                    const sc = getSpecialStarClass(s.name);
                    const sb = getSecondaryBrightness(s.name, palace.dia_chi);
                    const label = sb ? `${s.name} ${sb}` : s.name;
                    return sc
                        ? `<span class="aux-chip adj-star-chip ${sc}">${label}</span>`
                        : `<span class="aux-chip adj-star-chip" style="color:${getElementColor(STAR_ELEMENT_MAP[s.name])}">${label}</span>`;
                }).join('')}
            </div>`;
    }

    // TVF-1: Ring values (Tướng Tinh ring removed)
    if (palace.trang_sinh || palace.bac_si || palace.thai_tue) {
        html += `<div class="section-divider">Vòng Sao</div>
            <div class="ring-grid">
                <div class="ring-cell"><span class="ring-label">Tràng Sinh</span><span class="ring-value">${palace.trang_sinh || '—'}</span></div>
                <div class="ring-cell"><span class="ring-label">Bác Sĩ</span><span class="ring-value">${palace.bac_si || '—'}</span></div>
                <div class="ring-cell"><span class="ring-label">Thái Tuế</span><span class="ring-value">${palace.thai_tue || '—'}</span></div>
            </div>`;
    }

    // TVF-1: Đại Hạn section
    if (dh) {
        const isCurrent = dh.is_current ? '<span class="detail-badge-current">Đại Hạn hiện tại</span>' : '';
        html += `<div class="section-divider">Đại Hạn</div>
            <div class="detail-section">
                ${isCurrent}
                <p class="detail-interpretation">
                    Tuổi ${dh.range ? `${dh.range[0]}–${dh.range[1]}` : ''}
                    ${dh.can_chi ? `· ${dh.can_chi}` : ''}
                </p>
            </div>`;
    }

    // TVF-1: Tuần / Triệt warnings
    if (palace.tuan) {
        html += `<span class="detail-warning tuan-warning">旬空 Tuần</span>`;
    }
    if (palace.triet) {
        html += `<span class="detail-warning triet-warning">截路 Triệt</span>`;
    }

    // TVF-5: Per-palace interpret button
    html += `<div class="detail-interpret-wrap">
        <button class="btn-interpret-palace" onclick="interpretPalace(${palace.position})">✨ ${getPalaceButtonLabel(palace.cung_name)}</button>
    </div>`;

    return html;
}

function openDetailPanel(palace) {
    const html = buildDetailHTML(palace);

    if (window.innerWidth <= 600) {
        // Mobile: use bottom sheet
        if (typeof openBottomSheet === 'function') openBottomSheet(html);
        return;
    }

    // Desktop: side panel
    const panel   = document.getElementById('detail-panel');
    const overlay = document.getElementById('detail-overlay');
    const content = document.getElementById('detail-content');

    if (!panel || !content) return;
    content.innerHTML = html;
    panel.classList.add('open');
    if (overlay) overlay.classList.add('open');
}

function closeDetailPanel() {
    const panel   = document.getElementById('detail-panel');
    const overlay = document.getElementById('detail-overlay');
    if (panel)   panel.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
}

// =========================================
// LOADING / ERROR
// =========================================
function showLoading() {
    const container = document.getElementById('chart-container');
    if (container) container.innerHTML = '<div class="loading">' + t('tv.calculating_chart') + '</div>';
}

function showError(message) {
    const container = document.getElementById('chart-container');
    if (container) container.innerHTML = `<div class="loading" style="color:var(--error);">Lỗi: ${message}</div>`;
}

// =========================================
// FORM SUBMIT
// =========================================
async function handleSubmit(event) {
    event.preventDefault();

    const year   = parseInt(document.getElementById('year').value);
    const month  = parseInt(document.getElementById('month').value);
    const day    = parseInt(document.getElementById('day').value);
    const hour   = parseInt(document.getElementById('hour').value) || 0;
    const minute = parseInt(document.getElementById('minute').value) || 0;
    const gender = document.querySelector('input[name="gender"]:checked')?.value || 'nam';
    const namXemRaw = parseInt(document.getElementById('nam_xem')?.value);
    const nam_xem = namXemRaw && namXemRaw >= 1900 ? namXemRaw : null;

    if (!year || !month || !day) {
        showError(t('tv.error_complete_birthdate'));
        return;
    }

    showLoading();

    try {
        const data = await tuviApi.getChart(year, month, day, hour, minute, false, gender, nam_xem);
        renderChart(data);
    } catch (error) {
        console.error('Error loading chart:', error);
        showError(error.message);
    }
}

// =========================================
// AI INTERPRETATION — R5
// =========================================
async function interpretWithAI() {
    if (!currentTuviData) {
        alert(t('tv.error_view_chart_first'));
        return;
    }

    _showEnglishDisclaimerIfNeeded();

    const panel   = document.getElementById('ai-interpret-panel');
    const content = document.getElementById('ai-interpret-content');
    panel.classList.remove('hidden');
    panel.classList.add('slide-in');
    content.innerHTML = '<div class="ai-loading-dots"><div class="ai-loading-dot"></div><div class="ai-loading-dot"></div><div class="ai-loading-dot"></div></div>';
    panel.scrollIntoView({ behavior: 'smooth' });

    // X5-4: personalized badge
    const badge = document.getElementById('personalized-badge');
    if (badge) {
        badge.classList.toggle('hidden', !localStorage.getItem('tuvi_profile'));
    }

    const birth_info = {
        year:   parseInt(document.getElementById('year').value),
        month:  parseInt(document.getElementById('month').value),
        day:    parseInt(document.getElementById('day').value),
        hour:   parseInt(document.getElementById('hour').value) || 0,
        minute: parseInt(document.getElementById('minute').value) || 0,
        gender: document.querySelector('input[name="gender"]:checked')?.value || 'nam'
    };

    let static_interpretation = "## Tổng quan lá số\n\n";
    for (const palace of (currentTuviData.palaces || [])) {
        const cungName = palace.cung_name;
        const stars    = palace.stars || [];
        static_interpretation += `### Cung ${palace.position}. ${cungName}\n`;
        if (palace.meaning) static_interpretation += `${palace.meaning}\n`;
        if (stars.length)   static_interpretation += `**Các sao:** ${stars.map(s => s.name).join(', ')}\n`;
        static_interpretation += '\n';
    }

    try {
        const deviceId = getDeviceId('tuvi_device_id');
        const response = await fetch(`${API_BASE}/api/tuvi/interpret/stream?device_id=${encodeURIComponent(deviceId)}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                birth_info,
                chart_data: currentTuviData,
                static_interpretation,
                question: "Hãy luận giải chi tiết lá số của tôi"
            })
        });

        if (!response.ok) throw new Error('Interpretation failed');

        content.innerHTML = '';
        await readSSEStream(response, content, { appName: 'tuvi', readingId: 'yearly_' + Date.now().toString(36) });
        if (typeof renderFeedbackButtons === 'function') {
            const fbDiv = document.createElement('div');
            fbDiv.className = 'reading-feedback-container';
            content.appendChild(fbDiv);
            renderFeedbackButtons(fbDiv, 'yearly_' + Date.now().toString(36), 'tuvi');
        }
    } catch (e) {
        console.error('Interpretation error:', e);
        content.innerHTML = `<p style="color:var(--error);">Lỗi: ${e.message}</p>`;
    }
}

function closeAIPanel() {
    const panel = document.getElementById('ai-interpret-panel');
    if (panel) {
        panel.classList.add('hidden');
        panel.classList.remove('slide-in');
    }
}

// =========================================
// MARKDOWN RENDERER
// =========================================
function parseMarkdown(text) { return renderMarkdown(text); }

// =========================================
// CMP-2: HỢP DUYÊN COMPATIBILITY
// =========================================

let _cmpGenderA = 'nam';
let _cmpGenderB = 'nu';
let _cmpOpen = false;

const HOUR_OPTIONS_HTML = Array.from({ length: 24 }, (_, h) =>
    `<option value="${h}">${String(h).padStart(2,'0')}:00</option>`
).join('');

function initCmpHourSelects() {
    const selA = document.getElementById('cmp-a-hour');
    const selB = document.getElementById('cmp-b-hour');
    if (selA && !selA.children.length) selA.innerHTML = HOUR_OPTIONS_HTML;
    if (selB && !selB.children.length) selB.innerHTML = HOUR_OPTIONS_HTML;
}

function toggleCompatibilitySection() {
    const panel = document.getElementById('cmp-panel');
    if (!panel) return;
    _cmpOpen = !_cmpOpen;
    if (_cmpOpen) {
        panel.classList.remove('hidden');
        initCmpHourSelects();
        autoFillPersonAFromProfile();
    } else {
        panel.classList.add('hidden');
    }
}

function autoFillPersonAFromProfile() {
    try {
        const raw = typeof localStorage !== 'undefined' && localStorage.getItem('tuvi_profile');
        if (!raw) return;
        const profile = JSON.parse(raw);
        if (!profile) return;
        if (profile.name) {
            const el = document.getElementById('cmp-a-name');
            if (el && !el.value) el.value = profile.name;
        }
        if (profile.birth_date) {
            // birth_date stored as 'dd/mm/yyyy' per lt-memory feedback
            const parts = profile.birth_date.split('/');
            if (parts.length === 3) {
                const dayEl   = document.getElementById('cmp-a-day');
                const monEl   = document.getElementById('cmp-a-month');
                const yearEl  = document.getElementById('cmp-a-year');
                if (dayEl  && !dayEl.value)  dayEl.value  = parts[0];
                if (monEl  && !monEl.value)  monEl.value  = parts[1];
                if (yearEl && !yearEl.value) yearEl.value = parts[2];
            }
        }
        if (profile.gender) selectCompatibilityGender('a', profile.gender === 'male' ? 'nam' : profile.gender);
    } catch (e) { /* ignore */ }
}

function selectCompatibilityGender(person, gender) {
    if (person === 'a') _cmpGenderA = gender;
    else                _cmpGenderB = gender;
    document.querySelectorAll(`.cmp-gender-btn[data-person="${person}"]`).forEach(btn => {
        btn.classList.toggle('active', btn.dataset.gender === gender);
    });
}

async function submitCompatibility() {
    const loading = document.getElementById('cmp-loading');
    const errEl   = document.getElementById('cmp-error');
    const results = document.getElementById('cmp-results');

    if (loading) loading.classList.remove('hidden');
    if (errEl)   errEl.classList.add('hidden');
    if (results) results.classList.add('hidden');

    const personA = {
        name:   (document.getElementById('cmp-a-name')?.value  || '').trim(),
        year:   parseInt(document.getElementById('cmp-a-year')?.value)  || 0,
        month:  parseInt(document.getElementById('cmp-a-month')?.value) || 0,
        day:    parseInt(document.getElementById('cmp-a-day')?.value)   || 0,
        hour:   parseInt(document.getElementById('cmp-a-hour')?.value)  || 0,
        gender: _cmpGenderA,
    };
    const personB = {
        name:   (document.getElementById('cmp-b-name')?.value  || '').trim(),
        year:   parseInt(document.getElementById('cmp-b-year')?.value)  || 0,
        month:  parseInt(document.getElementById('cmp-b-month')?.value) || 0,
        day:    parseInt(document.getElementById('cmp-b-day')?.value)   || 0,
        hour:   parseInt(document.getElementById('cmp-b-hour')?.value)  || 0,
        gender: _cmpGenderB,
    };

    try {
        const deviceId = typeof getDeviceId === 'function' ? getDeviceId('tuvi_device_id') : '';
        const res = await fetch(`${API_BASE}/api/tuvi/compatibility`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ person_a: personA, person_b: personB, device_id: deviceId }),
        });
        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            throw new Error(data.detail || `HTTP ${res.status}`);
        }
        const data = await res.json();
        if (loading) loading.classList.add('hidden');
        renderCompatibilityResult(data);
        streamCompatibilityAnalysis(data);
    } catch (e) {
        if (loading) loading.classList.add('hidden');
        if (errEl) {
            errEl.textContent = 'Lỗi: ' + e.message;
            errEl.classList.remove('hidden');
        }
    }
}

const CMP_SCORE_CLASSES = [
    { min: 80, cls: 'score-excellent' },
    { min: 60, cls: 'score-good' },
    { min: 40, cls: 'score-neutral' },
    { min: 20, cls: 'score-caution' },
    { min: 0,  cls: 'score-hard' },
];

function renderCompatibilityResult(data) {
    // Score circle
    const circle   = document.getElementById('cmp-score-circle');
    const valueEl  = document.getElementById('cmp-score-value');
    const ratingEl = document.getElementById('cmp-score-rating');
    if (valueEl)  valueEl.textContent  = String(data.score);
    if (ratingEl) ratingEl.textContent = data.rating || '';
    if (circle) {
        CMP_SCORE_CLASSES.forEach(({ cls }) => circle.classList.remove(cls));
        const match = CMP_SCORE_CLASSES.find(({ min }) => data.score >= min);
        if (match) circle.classList.add(match.cls);
    }

    // Factor bars (25pts max each)
    const FACTOR_MAP = [
        { id: 'cmp-factor-ngu-hanh', key: 'ngu_hanh' },
        { id: 'cmp-factor-zodiac',   key: 'zodiac' },
        { id: 'cmp-factor-phu-the',  key: 'phu_the' },
        { id: 'cmp-factor-menh',     key: 'menh_harmony' },
    ];
    const factors = data.factors || {};
    FACTOR_MAP.forEach(({ id, key }) => {
        const barEl    = document.getElementById(id);
        if (!barEl) return;
        const factor   = factors[key] || { score: 0, detail: '' };
        const fill     = barEl.querySelector('.cmp-factor-fill');
        const detail   = barEl.querySelector('.cmp-factor-detail');
        const pct      = Math.round((factor.score / 25) * 100);
        if (fill)   fill.style.width   = `${pct}%`;
        if (detail) detail.textContent = factor.detail || '';
    });

    // Show results panel
    const results = document.getElementById('cmp-results');
    if (results) results.classList.remove('hidden');
}

async function streamCompatibilityAnalysis(data) {
    const content = document.getElementById('cmp-analysis-content');
    if (!content) return;

    content.innerHTML = '<div style="color:var(--text-muted);font-size:0.8rem;padding:8px 0">Đang luận giải<span class="dots"></span></div>';

    try {
        const deviceId = typeof getDeviceId === 'function' ? getDeviceId('tuvi_device_id') : '';
        const res = await fetch(`${API_BASE}/api/tuvi/compatibility/stream`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...data, device_id: deviceId }),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        content.innerHTML = '';
        await readSSEStream(res, content, { appName: 'tuvi', readingId: 'compat_' + Date.now().toString(36) });
        if (typeof renderFeedbackButtons === 'function') {
            const fbDiv = document.createElement('div');
            fbDiv.className = 'reading-feedback-container';
            content.appendChild(fbDiv);
            renderFeedbackButtons(fbDiv, 'compat_' + Date.now().toString(36), 'tuvi');
        }
    } catch (e) {
        content.innerHTML = `<p style="color:var(--error)">Lỗi luận giải: ${e.message}</p>`;
    }
}

// Show CMP button when chart is ready (called from renderChart)
function showCompatibilityButton() {
    const el = document.getElementById('cmp-section');
    if (el) el.classList.remove('hidden');
}

// =========================================
// LN-2: LƯU NIÊN YEARLY FORECAST
// =========================================

let _luuNienYear = new Date().getFullYear();
let _luuNienOpen = false;

function initLuuNienYearSelect() {
    const sel = document.getElementById('ln-year-select');
    if (!sel) return;
    const now = new Date().getFullYear();
    sel.innerHTML = '';
    for (let y = now - 5; y <= now + 5; y++) {
        const opt = document.createElement('option');
        opt.value = y;
        opt.textContent = y;
        if (y === _luuNienYear) opt.selected = true;
        sel.appendChild(opt);
    }
}

function toggleLuuNienSection() {
    const panel = document.getElementById('ln-panel');
    if (!panel) return;
    _luuNienOpen = !_luuNienOpen;
    if (_luuNienOpen) {
        panel.classList.remove('hidden');
        initLuuNienYearSelect();
        loadYearlyForecast(_luuNienYear);
    } else {
        panel.classList.add('hidden');
    }
}

function onYearSelectChange() {
    const sel = document.getElementById('ln-year-select');
    if (!sel) return;
    _luuNienYear = parseInt(sel.value, 10);
    return loadYearlyForecast(_luuNienYear);
}

function changeYear(delta) {
    _luuNienYear += delta;
    const sel = document.getElementById('ln-year-select');
    if (sel) sel.value = _luuNienYear;
    loadYearlyForecast(_luuNienYear);
}

async function loadYearlyForecast(year) {
    const loading = document.getElementById('ln-loading');
    const errEl   = document.getElementById('ln-error');
    const overview = document.getElementById('ln-overview');
    const grid    = document.getElementById('ln-month-grid');
    const detail  = document.getElementById('ln-month-detail');

    if (loading)  loading.classList.remove('hidden');
    if (errEl)    errEl.classList.add('hidden');
    if (overview) overview.classList.add('hidden');
    if (grid)     grid.innerHTML = '';
    if (detail)   detail.classList.add('hidden');

    try {
        const deviceId = typeof getDeviceId === 'function' ? getDeviceId('tuvi_device_id') : '';
        const url = `/api/tuvi/forecast/yearly?year=${year}&device_id=${encodeURIComponent(deviceId)}`;
        const res = await fetch(url);
        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            throw new Error(data.detail || `HTTP ${res.status}`);
        }
        const data = await res.json();
        if (loading) loading.classList.add('hidden');
        renderYearlyForecast(data);
    } catch (e) {
        if (loading) loading.classList.add('hidden');
        if (errEl) {
            errEl.textContent = 'Lỗi: ' + e.message;
            errEl.classList.remove('hidden');
        }
    }
}

function renderYearlyForecast(data) {
    // Overview card
    const titleEl  = document.getElementById('ln-year-title');
    const ageEl    = document.getElementById('ln-nominal-age');
    const menhEl   = document.getElementById('ln-menh-palace');
    const tuHoaEl  = document.getElementById('ln-tuhoa');
    const overview = document.getElementById('ln-overview');

    if (titleEl)  titleEl.textContent  = `Năm ${data.year} — ${data.can_chi || ''}`;
    if (ageEl)    ageEl.textContent    = `Tuổi ${data.nominal_age || ''}`;
    if (menhEl)   menhEl.textContent   = `Lưu Niên Mệnh: ${(data.luu_nien && data.luu_nien.menh) || ''}`;
    if (tuHoaEl && data.luu_nien && data.luu_nien.tu_hoa) {
        const dotMap = { 'Lộc': 'loc', 'Quyền': 'quyen', 'Khoa': 'khoa', 'Kỵ': 'ky' };
        tuHoaEl.innerHTML = data.luu_nien.tu_hoa.map(s => {
            const dotClass = Object.entries(dotMap).find(([k]) => s.includes(k));
            const cls = dotClass ? dotClass[1] : '';
            return `<span class="ln-tuhoa-chip ${cls}">${s}</span>`;
        }).join('');
    }
    if (overview) overview.classList.remove('hidden');

    // Month grid
    const grid = document.getElementById('ln-month-grid');
    if (!grid || !data.months) return;
    grid.innerHTML = data.months.map((m, i) => {
        const rating = m.rating || 'neutral';
        const keyTuHoa = m.tu_hoa && m.tu_hoa[0] ? m.tu_hoa[0] : '';
        return `
        <div class="ln-month-card" data-month="${i}" onclick="showLuuNienDetail(${i})">
            <div class="ln-month-header">
                <span class="ln-month-name">Tháng ${m.month}</span>
                <span class="ln-rating-dot ${rating}"></span>
            </div>
            <div class="ln-month-palace">${m.luu_nguyet_menh || ''}</div>
            <div class="ln-month-tuhoa">${keyTuHoa}</div>
        </div>`;
    }).join('');

    // Store data for detail panel
    document.getElementById('ln-month-grid')._monthsData = data.months;
}

function showLuuNienDetail(monthIndex) {
    const grid   = document.getElementById('ln-month-grid');
    const detail = document.getElementById('ln-month-detail');
    const titleEl = document.getElementById('ln-detail-title');
    const bodyEl  = document.getElementById('ln-detail-body');
    if (!grid || !detail) return;

    const months = grid._monthsData;
    if (!months || !months[monthIndex]) return;
    const m = months[monthIndex];

    // Highlight active card
    grid.querySelectorAll('.ln-month-card').forEach((c, i) => {
        c.classList.toggle('active', i === monthIndex);
    });

    if (titleEl) titleEl.textContent = `Tháng ${m.month}`;

    const ratingLabel = { good: '✦ Tốt', neutral: '○ Bình thường', caution: '⚠ Thận trọng' };
    const tuHoaText = (m.tu_hoa || []).join(' · ') || '—';

    if (bodyEl) bodyEl.innerHTML = `
        <div class="ln-detail-body-row">
            <span class="ln-detail-label">Đánh giá:</span>
            <span class="ln-detail-value">${ratingLabel[m.rating] || m.rating}</span>
        </div>
        <div class="ln-detail-body-row">
            <span class="ln-detail-label">Lưu Nguyệt Mệnh:</span>
            <span class="ln-detail-value">${m.luu_nguyet_menh || '—'}</span>
        </div>
        <div class="ln-detail-body-row">
            <span class="ln-detail-label">Tứ Hóa:</span>
            <span class="ln-detail-value">${tuHoaText}</span>
        </div>
        <div class="ln-detail-body-row">
            <span class="ln-detail-label">Sao nổi bật:</span>
            <span class="ln-detail-value">${(m.key_stars || []).join(', ') || '—'}</span>
        </div>`;

    detail.classList.remove('hidden');
    if (detail.scrollIntoView) detail.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function closeLuuNienDetail() {
    const detail = document.getElementById('ln-month-detail');
    if (detail) detail.classList.add('hidden');
    const grid = document.getElementById('ln-month-grid');
    if (grid) grid.querySelectorAll('.ln-month-card').forEach(c => c.classList.remove('active'));
}

// Called from renderChart() to show the LN button when chart is ready
function showLuuNienButton() {
    const el = document.getElementById('ln-section');
    if (el) el.classList.remove('hidden');
}

// CommonJS export for Jest tests (no-op in browser)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
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
        renderChart,
        renderTimeline,
        openDetailPanel,
        closeDetailPanel,
        showLoading,
        showError,
        handleSubmit,
        interpretWithAI,
        closeAIPanel,
        _setCurrentTuviData: (d) => { currentTuviData = d; },
        _setCurrentChartData: (d) => { currentChartData = d; },
        // CMP-2 exports
        toggleCompatibilitySection,
        autoFillPersonAFromProfile,
        selectCompatibilityGender,
        submitCompatibility,
        renderCompatibilityResult,
        streamCompatibilityAnalysis,
        showCompatibilityButton,
        _getCmpGenderA: () => _cmpGenderA,
        _getCmpGenderB: () => _cmpGenderB,
        // LN-2 exports
        initLuuNienYearSelect,
        toggleLuuNienSection,
        onYearSelectChange,
        changeYear,
        loadYearlyForecast,
        renderYearlyForecast,
        showLuuNienDetail,
        closeLuuNienDetail,
        showLuuNienButton,
        _getLuuNienYear: () => _luuNienYear,
        _setLuuNienYear: (y) => { _luuNienYear = y; },
        _getLuuNienOpen: () => _luuNienOpen,
        _setLuuNienOpen: (v) => { _luuNienOpen = v; },
    };
}

// =========================================
// INIT
// =========================================
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('tuvi-form');
    if (form) form.addEventListener('submit', handleSubmit);

    const overlay = document.getElementById('detail-overlay');
    if (overlay) overlay.addEventListener('click', closeDetailPanel);

});

function _showEnglishDisclaimerIfNeeded() {
    const disclaimer = document.getElementById('english-disclaimer');
    if (!disclaimer) return;
    const locale = typeof getLocale === 'function' ? getLocale() : 'vi';
    if (locale === 'en') {
        disclaimer.classList.remove('hidden');
    } else {
        disclaimer.classList.add('hidden');
    }
}

// =========================================
// LUẬN GIẢI LÁ SỐ
// =========================================
function toggleLuanGiai() {
    const panel = document.getElementById('lg-panel');
    if (!panel) return;

    if (panel.classList.contains('hidden')) {
        // Render nếu chưa có
        if (!panel.innerHTML.trim() && currentChartData && typeof buildLuanGiaiHTML === 'function') {
            panel.innerHTML = buildLuanGiaiHTML(currentChartData);
        }
        panel.classList.remove('hidden');
    } else {
        panel.classList.add('hidden');
    }
}
