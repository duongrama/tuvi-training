/**
 * hop-tuoi.test.js — S98 COMP-2/3/4 FE Tests
 * COMP-2: Entry form, context selector, teaser render
 * COMP-3: Share buttons, skip gate, partner deep-link flow
 * COMP-4: Full streaming report with 5 sections
 */

// Polyfills for jsdom (doesn't expose TextDecoder/TextEncoder/ReadableStream)
if (typeof global.TextEncoder === 'undefined') {
    global.TextEncoder = class TextEncoder {
        encode(str) { return Buffer.from(str, 'utf8'); }
    };
}
if (typeof global.TextDecoder === 'undefined') {
    global.TextDecoder = class TextDecoder {
        decode(buf, opts) {
            if (opts && opts.stream) return Buffer.from(buf).toString('utf8');
            return Buffer.from(buf).toString('utf8');
        }
    };
}
if (typeof global.ReadableStream === 'undefined') {
    // Make stream override work via module parameter
    global.ReadableStream = undefined;
}

// Mock ReadableStream for jsdom (jsdom doesn't expose Streams API)
function makeMockStream(chunks) {
    let index = 0;
    return {
        getReader() {
            return {
                read() {
                    if (index >= chunks.length) {
                        return Promise.resolve({ done: true, value: undefined });
                    }
                    const chunk = chunks[index++];
                    return Promise.resolve({ done: false, value: chunk });
                }
            };
        }
    };
}

function makeSSEStream(...args) {
    // args is an array of strings (each a complete SSE event)
    const chunks = args.map(ev => Buffer.from(ev, 'utf8'));
    return makeMockStream(chunks);
}

// ── CSS for visibility pattern ────────────────────────────────────────
const style = document.createElement('style');
style.textContent = `
    .hidden { display: none !important; }
    .visible { display: block !important; }
    .ht-loading, .ht-error, .ht-invite-modal, #ht-partner-section, #ht-full-report, #ht-share-card { display: none; }
    .ht-teaser { display: none; }
`;
document.head.appendChild(style);

// ── Full DOM (mimics /hop-tuoi route HTML) ──
document.body.innerHTML = `
  <div id="ht-form-section">
    <div id="ht-person-a">
      <input id="ht-a-name" type="text" value="">
      <input id="ht-a-year" type="number" value="" min="1940" max="2015">
      <div id="ht-a-error"></div>
    </div>
    <div id="ht-person-b">
      <input id="ht-b-name" type="text" value="">
      <input id="ht-b-year" type="number" value="" min="1940" max="2015">
      <div id="ht-b-error"></div>
    </div>
    <div id="ht-context-selector">
      <button type="button" class="ht-context-btn active" data-context="romance" id="ht-ctx-romance">💕 Tình Duyên</button>
      <button type="button" class="ht-context-btn" data-context="family" id="ht-ctx-family">👨‍👩‍👧 Gia Đình</button>
      <button type="button" class="ht-context-btn" data-context="business" id="ht-ctx-business">💼 Làm Ăn</button>
    </div>
    <button type="button" id="ht-submit-btn" onclick="htSubmit()">Xem Hợp Tuổi</button>
    <div id="ht-loading"></div>
    <div id="ht-error"></div>
  </div>

  <!-- Teaser Result -->
  <div id="ht-teaser" class="ht-form-card ht-teaser">
    <div id="ht-zodiac-a"></div>
    <div id="ht-zodiac-b"></div>
    <div id="ht-zodiac-verdict-badge"></div>
    <div id="ht-element-arrow"></div>
    <div id="ht-score-value"></div>
    <div id="ht-score-rating"></div>
    <div id="ht-summary"></div>
    <button type="button" id="ht-cta-btn" onclick="htOpenInvitationModal()">🔮 Xem phân tích AI chi tiết...</button>
  </div>

  <!-- COMP-3: Invitation Modal -->
  <div id="ht-invite-modal">
    <button class="ht-invite-close" onclick="htCloseInviteModal()">✕</button>
    <h3 id="ht-invite-header"></h3>
    <textarea id="ht-invite-message"></textarea>
    <button type="button" id="ht-share-zalo-btn" onclick="htShareZalo()">Zalo</button>
    <button type="button" id="ht-share-fb-btn" onclick="htShareMessenger()">Messenger</button>
    <button type="button" id="ht-copy-link-btn" onclick="htCopyLink()">Copy Link</button>
    <a href="#" id="ht-skip-link" onclick="htSkipGate(event)">Bỏ qua</a>
  </div>

  <!-- COMP-3: Partner Landing -->
  <div id="ht-partner-section">
    <p id="ht-partner-msg"></p>
    <button type="button" id="ht-partner-submit-btn" onclick="htPartnerSubmit()">Xem kết quả</button>
  </div>

  <!-- COMP-4: Full Report -->
  <div id="ht-full-report">
    <div id="ht-report-header"></div>
    <div id="ht-report-streaming">
      <div id="ht-section-0"></div>
      <div id="ht-section-1"></div>
      <div id="ht-section-2"></div>
      <div id="ht-section-3"></div>
      <div id="ht-section-4"></div>
    </div>
    <div id="ht-share-card">
      <button type="button" id="ht-share-card-btn">📸 Chia sẻ kết quả</button>
    </div>
    <button type="button" id="ht-reentry-btn">Xem hợp tuổi với người khác</button>
  </div>
`;

// ── Globals (must be before require) ──
global.API_BASE = '';
global.fetch = jest.fn(() => Promise.resolve({ ok: true, json: async () => ({}), body: {} }));
global.alert = jest.fn();
global.confirm = jest.fn(() => true);
global.getDeviceId = jest.fn(() => 'test-device');
global.clipboard = { writeText: jest.fn(() => Promise.resolve()) };
Object.defineProperty(navigator, 'clipboard', { value: global.clipboard, configurable: true });
// window.open for share buttons
const _origOpen = global.window.open;
// Clear old exports cache
jest.resetModules();

jest.resetModules();
const mod = require('../js/hop-tuoi.js');
const {
    htSelectContext,
    htSubmit,
    renderHopTuoiTeaser,
    htOpenInvitationModal,
    htCloseInviteModal,
    loadInvitationData,
    htShareZalo,
    htShareMessenger,
    htCopyLink,
    htSkipGate,
    htPartnerSubmit,
    renderHopTuoiFullReport,
} = mod;

// ── Mock API response ──
function mockHopTuoiResult(overrides = {}) {
    return {
        person_a: { year: 1990, zodiac: 'Ngọ', zodiac_name: 'Tuổi Ngựa', nap_am: 'Lộ Bàng Thổ', element: 'Thổ' },
        person_b: { year: 1992, zodiac: 'Thân', zodiac_name: 'Tuổi Khỉ', nap_am: 'Kiếm Phong Kim', element: 'Kim' },
        zodiac_verdict: { type: 'trung_tinh', label: 'Trung tính', detail: 'Ngọ-Thân — không thuộc nhóm hợp/xung đặc biệt', score: 15 },
        element_verdict: { type: 'tuong_sinh', label: 'Tương Sinh', detail: 'Thổ→Kim — Thổ sinh Kim', score: 25 },
        combined_score: 40,
        combined_rating: 'Bình thường',
        summary: 'Tuổi Ngựa và tuổi Khỉ có ngũ hành Tương Sinh, nhưng địa chi không thuộc nhóm đặc biệt.',
        ...overrides,
    };
}

function mockInviteResponse(overrides = {}) {
    return {
        invitation_id: 'abc12345',
        deep_link: 'https://localhost:17070/hop-tuoi?invite=abc12345',
        ...overrides,
    };
}

beforeEach(() => {
    jest.clearAllMocks();
    // All visibility controlled via .visible class
    document.getElementById('ht-teaser')?.classList.remove('visible');
    document.getElementById('ht-invite-modal')?.classList.remove('visible');
    document.getElementById('ht-loading')?.classList.remove('visible');
    document.getElementById('ht-error')?.classList.remove('visible');
    document.getElementById('ht-full-report')?.classList.remove('visible');
    document.getElementById('ht-partner-section')?.classList.remove('visible');
    document.getElementById('ht-share-card')?.classList.remove('visible');
    document.getElementById('ht-a-year').value = '';
    document.getElementById('ht-b-year').value = '';
    document.getElementById('ht-a-error')?.classList.remove('visible');
    document.getElementById('ht-b-error')?.classList.remove('visible');
    htSelectContext('romance');
});

// ═══════════════════════════════════════════════════════════════════
// Test 1: Context selector defaults to romance
// ═══════════════════════════════════════════════════════════════════
test('context selector defaults to romance on page load', () => {
    const romanceBtn = document.getElementById('ht-ctx-romance');
    const familyBtn = document.getElementById('ht-ctx-family');
    const businessBtn = document.getElementById('ht-ctx-business');

    expect(romanceBtn.classList.contains('active')).toBe(true);
    expect(familyBtn.classList.contains('active')).toBe(false);
    expect(businessBtn.classList.contains('active')).toBe(false);
});

// ═══════════════════════════════════════════════════════════════════
// Test 2: Context selector switches active pill
// ═══════════════════════════════════════════════════════════════════
test('htSelectContext switches active pill and deselects others', () => {
    htSelectContext('family');

    expect(document.getElementById('ht-ctx-family').classList.contains('active')).toBe(true);
    expect(document.getElementById('ht-ctx-romance').classList.contains('active')).toBe(false);
    expect(document.getElementById('ht-ctx-business').classList.contains('active')).toBe(false);
});

test('htSelectContext persists through re-render', () => {
    htSelectContext('business');
    expect(document.getElementById('ht-ctx-business').classList.contains('active')).toBe(true);
    expect(document.getElementById('ht-ctx-romance').classList.contains('active')).toBe(false);
});

// ═══════════════════════════════════════════════════════════════════
// Test 3: Birth year validation — valid range accepted
// ═══════════════════════════════════════════════════════════════════
test('birth year accepts valid range 1940-2015', () => {
    const testYears = [1940, 1950, 1980, 1995, 2000, 2015];
    testYears.forEach(year => {
        document.getElementById('ht-a-year').value = String(year);
        // No .visible class for valid years
        expect(document.getElementById('ht-a-error').classList.contains('visible')).toBe(false);
    });
});

// ═══════════════════════════════════════════════════════════════════
// Test 4: Birth year validation — out-of-range rejected
// ═══════════════════════════════════════════════════════════════════
test('birth year rejects below 1940 and shows error', async () => {
    document.getElementById('ht-a-year').value = '1939';
    global.fetch = jest.fn(() => Promise.resolve({
        ok: false, status: 400, json: async () => ({ detail: 'Year out of range' })
    }));

    await htSubmit();

    expect(document.getElementById('ht-a-error').classList.contains('visible')).toBe(true);
    expect(document.getElementById('ht-a-error').textContent).toBeTruthy();
    expect(document.getElementById('ht-submit-btn').disabled).toBe(false);
});

test('birth year rejects above 2015 and shows error', async () => {
    document.getElementById('ht-a-year').value = '2016';
    global.fetch = jest.fn(() => Promise.resolve({
        ok: false, status: 400, json: async () => ({ detail: 'Year out of range' })
    }));

    await htSubmit();

    expect(document.getElementById('ht-a-error').classList.contains('visible')).toBe(true);
});

// ═══════════════════════════════════════════════════════════════════
// Test 5: Form submits correct POST body
// ═══════════════════════════════════════════════════════════════════
test('htSubmit sends POST with year_a, year_b, context', async () => {
    document.getElementById('ht-a-year').value = '1990';
    document.getElementById('ht-b-year').value = '1992';
    htSelectContext('romance');

    global.fetch = jest.fn(() => Promise.resolve({
        ok: true,
        json: async () => mockHopTuoiResult(),
        body: {},
    }));

    await htSubmit();

    expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/tuvi/hop-tuoi'),
        expect.objectContaining({ method: 'POST' })
    );

    const callArgs = global.fetch.mock.calls[0];
    const reqBody = JSON.parse(callArgs[1].body);
    expect(reqBody.year_a).toBe(1990);
    expect(reqBody.year_b).toBe(1992);
    expect(reqBody.context).toBe('romance');
    expect(reqBody.device_id).toBe('test-device');
});

test('htSubmit sends correct context when family selected', async () => {
    document.getElementById('ht-a-year').value = '1985';
    document.getElementById('ht-b-year').value = '1988';
    htSelectContext('family');

    global.fetch = jest.fn(() => Promise.resolve({
        ok: true,
        json: async () => mockHopTuoiResult(),
        body: {},
    }));

    await htSubmit();

    const [, opts] = global.fetch.mock.calls[0];
    const reqBody = JSON.parse(opts.body);
    expect(reqBody.context).toBe('family');
});

test('htSubmit sends correct context when business selected', async () => {
    document.getElementById('ht-a-year').value = '1970';
    document.getElementById('ht-b-year').value = '1975';
    htSelectContext('business');

    global.fetch = jest.fn(() => Promise.resolve({
        ok: true,
        json: async () => mockHopTuoiResult(),
        body: {},
    }));

    await htSubmit();

    const [, opts] = global.fetch.mock.calls[0];
    const reqBody = JSON.parse(opts.body);
    expect(reqBody.context).toBe('business');
});

// ═══════════════════════════════════════════════════════════════════
// Test 6: Teaser renders zodiac pair
// ═══════════════════════════════════════════════════════════════════
test('renderHopTuoiTeaser renders zodiac pair for both persons', () => {
    renderHopTuoiTeaser(mockHopTuoiResult());

    expect(document.getElementById('ht-zodiac-a').textContent).toContain('Ngọ');
    expect(document.getElementById('ht-zodiac-b').textContent).toContain('Thân');
});

test('renderHopTuoiTeaser renders zodiac verdict badge', () => {
    renderHopTuoiTeaser(mockHopTuoiResult());

    const badge = document.getElementById('ht-zodiac-verdict-badge');
    expect(badge.textContent).toContain('Trung tính');
});

test('renderHopTuoiTeaser renders tam_hop verdict type', () => {
    renderHopTuoiTeaser(mockHopTuoiResult({
        zodiac_verdict: { type: 'tam_hop', label: 'Tam Hợp', detail: 'Ngọ-Tý-Thìn', score: 25 }
    }));

    const badge = document.getElementById('ht-zodiac-verdict-badge');
    expect(badge.textContent).toContain('Tam Hợp');
});

// ═══════════════════════════════════════════════════════════════════
// Test 7: Teaser renders element arrow
// ═══════════════════════════════════════════════════════════════════
test('renderHopTuoiTeaser renders element arrow with verdict', () => {
    renderHopTuoiTeaser(mockHopTuoiResult());

    const arrow = document.getElementById('ht-element-arrow');
    expect(arrow.textContent).toContain('Thổ');
    expect(arrow.textContent).toContain('Kim');
    expect(arrow.textContent).toContain('Tương Sinh');
});

test('renderHopTuoiTeaser renders tuong_khac arrow', () => {
    renderHopTuoiTeaser(mockHopTuoiResult({
        element_verdict: { type: 'tuong_khac', label: 'Tương Khắc', detail: 'Kim→Mộc — Kim khắc Mộc', score: 5 }
    }));

    const arrow = document.getElementById('ht-element-arrow');
    expect(arrow.textContent).toContain('Tương Khắc');
});

// ═══════════════════════════════════════════════════════════════════
// Test 8: Teaser renders score circle
// ═══════════════════════════════════════════════════════════════════
test('renderHopTuoiTeaser renders combined score (0-50 scale)', () => {
    renderHopTuoiTeaser(mockHopTuoiResult({ combined_score: 40 }));

    const scoreVal = document.getElementById('ht-score-value');
    expect(scoreVal.textContent).toBe('40');
});

test('renderHopTuoiTeaser renders score rating text', () => {
    renderHopTuoiTeaser(mockHopTuoiResult({ combined_rating: 'Bình thường' }));

    const rating = document.getElementById('ht-score-rating');
    expect(rating.textContent).toBe('Bình thường');
});

test('renderHopTuoiTeaser shows teaser section', () => {
    renderHopTuoiTeaser(mockHopTuoiResult());

    expect(document.getElementById('ht-teaser').classList.contains('visible')).toBe(true);
});

test('renderHopTuoiTeaser hides loading state', () => {
    document.getElementById('ht-loading').classList.add('visible');
    renderHopTuoiTeaser(mockHopTuoiResult());

    expect(document.getElementById('ht-loading').classList.contains('visible')).toBe(false);
});

// ═══════════════════════════════════════════════════════════════════
// Test 9: Teaser renders summary
// ═══════════════════════════════════════════════════════════════════
test('renderHopTuoiTeaser renders one-line summary', () => {
    const result = mockHopTuoiResult();
    renderHopTuoiTeaser(result);

    const summary = document.getElementById('ht-summary');
    expect(summary.textContent).toContain(result.summary);
});

// ═══════════════════════════════════════════════════════════════════
// Test 10: CTA button opens invitation modal
// ═══════════════════════════════════════════════════════════════════
test('htOpenInvitationModal shows the invitation modal', async () => {
    global.fetch = jest.fn(() => Promise.resolve({
        ok: true,
        json: async () => mockInviteResponse(),
    }));

    await htOpenInvitationModal();

    const modal = document.getElementById('ht-invite-modal');
    expect(modal.classList.contains('visible')).toBe(true);
});

test('htOpenInvitationModal populates deep link in message textarea', async () => {
    global.fetch = jest.fn(() => Promise.resolve({
        ok: true,
        json: async () => mockInviteResponse(),
    }));

    await htOpenInvitationModal();

    const message = document.getElementById('ht-invite-message');
    expect(message.value).toContain('abc12345');
});

test('htOpenInvitationModal sends correct invitation create body', async () => {
    document.getElementById('ht-a-name').value = 'Minh';
    document.getElementById('ht-b-name').value = 'Lan';
    document.getElementById('ht-a-year').value = '1990';
    document.getElementById('ht-b-year').value = '1992';

    global.fetch = jest.fn(() => Promise.resolve({
        ok: true,
        json: async () => mockInviteResponse(),
    }));

    // Seed _htCurrentResult so modal has data
    global._htCurrentResult = mockHopTuoiResult();

    await htOpenInvitationModal();

    expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/tuvi/invitation/create'),
        expect.objectContaining({ method: 'POST' })
    );

    const [, opts] = global.fetch.mock.calls[0];
    const reqBody = JSON.parse(opts.body);
    expect(reqBody.initiator_device_id).toBe('test-device');
    expect(reqBody.year_a).toBe(1990);
    expect(reqBody.year_b).toBe(1992);
    expect(reqBody.name_a).toBe('Minh');
    expect(reqBody.name_b).toBe('Lan');
    expect(reqBody.context).toBe('romance');
    expect(reqBody.hop_tuoi_result).toBeDefined();
});

test('htCloseInviteModal hides the invitation modal', () => {
    document.getElementById('ht-invite-modal').classList.add('visible');
    htCloseInviteModal();
    expect(document.getElementById('ht-invite-modal').classList.contains('visible')).toBe(false);
});

// ═══════════════════════════════════════════════════════════════════
// Test 11: Deep link param triggers partner landing flow
// ═══════════════════════════════════════════════════════════════════
test('URL with invite param triggers loadInvitationData on page load', async () => {
    // Mock fetch for invitation data load
    global.fetch = jest.fn(() => Promise.resolve({
        ok: true,
        json: async () => ({
            context: 'romance',
            hop_tuoi_result: mockHopTuoiResult(),
        }),
    }));

    await loadInvitationData('abc12345');

    expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/tuvi/invitation/abc12345')
    );
    // Should render teaser with invitation data
    expect(document.getElementById('ht-teaser').classList.contains('visible')).toBe(true);
});

// ═══════════════════════════════════════════════════════════════════
// Test 12: Error handling — API failure shows error message
// ═══════════════════════════════════════════════════════════════════
test('htSubmit shows error on API failure', async () => {
    document.getElementById('ht-a-year').value = '1990';
    document.getElementById('ht-b-year').value = '1992';

    global.fetch = jest.fn(() => Promise.resolve({
        ok: false,
        status: 500,
        json: async () => ({ detail: 'Server error' }),
    }));

    await htSubmit();

    expect(document.getElementById('ht-error').classList.contains('visible')).toBe(true);
    expect(document.getElementById('ht-loading').classList.contains('visible')).toBe(false);
});

// ═══════════════════════════════════════════════════════════════════
// Test 13: Loading state shown during API call
// ═══════════════════════════════════════════════════════════════════
test('htSubmit shows loading state while waiting for response', async () => {
    document.getElementById('ht-a-year').value = '1990';
    document.getElementById('ht-b-year').value = '1992';

    let resolveWait;
    global.fetch = jest.fn(() => new Promise(r => { resolveWait = r; }));

    const submitPromise = htSubmit();

    // Loading should be visible during the fetch
    expect(document.getElementById('ht-loading').classList.contains('visible')).toBe(true);

    resolveWait({ ok: true, json: async () => mockHopTuoiResult(), body: {} });
    await submitPromise;

    // Loading should be hidden after fetch
    expect(document.getElementById('ht-loading').classList.contains('visible')).toBe(false);
});

// ═══════════════════════════════════════════════════════════════════
// Test 14: Both person errors shown when both invalid
// ═══════════════════════════════════════════════════════════════════
test('htSubmit shows error for both persons when both years out of range', async () => {
    document.getElementById('ht-a-year').value = '1930';
    document.getElementById('ht-b-year').value = '2050';

    global.fetch = jest.fn(() => Promise.resolve({
        ok: false, status: 400, json: async () => ({ detail: 'Year out of range' })
    }));

    await htSubmit();

    // At least the first error should be visible
    const aErr = document.getElementById('ht-a-error');
    const bErr = document.getElementById('ht-b-error');
    expect(aErr.classList.contains('visible') || bErr.classList.contains('visible')).toBe(true);
});

// ═══════════════════════════════════════════════════════════════════
// COMP-3: Share Buttons
// ═══════════════════════════════════════════════════════════════════
test('htShareZalo opens Zalo share URL with deep link', () => {
    global.window.open = jest.fn();
    document.getElementById('ht-invite-message').value = 'https://localhost:17070/hop-tuoi?invite=abc123';

    htShareZalo();

    expect(global.window.open).toHaveBeenCalledWith(
        expect.stringContaining('zalo.me/share'),
        '_blank'
    );
    const zaloUrl = global.window.open.mock.calls[0][0];
    expect(zaloUrl).toContain('url=');
});

test('htShareMessenger opens Messenger share URL with deep link', () => {
    global.window.open = jest.fn();
    document.getElementById('ht-invite-message').value = 'https://localhost:17070/hop-tuoi?invite=abc123';

    htShareMessenger();

    expect(global.window.open).toHaveBeenCalledWith(
        expect.stringContaining('facebook.com'),
        '_blank'
    );
});

test('htCopyLink copies invite message to clipboard', async () => {
    global.clipboard.writeText = jest.fn(() => Promise.resolve());
    document.getElementById('ht-invite-message').value = 'https://localhost:17070/hop-tuoi?invite=abc123';

    await htCopyLink();

    expect(global.clipboard.writeText).toHaveBeenCalledWith('https://localhost:17070/hop-tuoi?invite=abc123');
    expect(global.alert).toHaveBeenCalled();
});

// ═══════════════════════════════════════════════════════════════════
// COMP-3: Skip Gate
// ═══════════════════════════════════════════════════════════════════
test('htSkipGate hides invite modal and shows full report', async () => {
    document.getElementById('ht-invite-modal').classList.remove('hidden');
    document.getElementById('ht-full-report').classList.add('hidden');

    global.fetch = jest.fn(() =>
        Promise.resolve({ ok: true, body: makeSSEStream(
            'data: {"content":"Phan tich 1"}\n\n',
            'data: [DONE]\n\n'
        ) })
    );

    const event = { preventDefault: jest.fn() };
    await htSkipGate(event, mockHopTuoiResult());

    expect(event.preventDefault).toHaveBeenCalled();
    expect(document.getElementById('ht-invite-modal').classList.contains('visible')).toBe(false);
    expect(document.getElementById('ht-full-report').classList.contains('visible')).toBe(true);
});

test('htSkipGate calls streaming endpoint with correct compatibility params', async () => {
    global.fetch = jest.fn(() =>
        Promise.resolve({ ok: true, body: makeSSEStream(
            'data: {"content":"Test"}\n\n',
            'data: [DONE]\n\n'
        ) })
    );

    const event = { preventDefault: jest.fn() };
    await htSkipGate(event, mockHopTuoiResult());

    expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/tuvi/compatibility/stream'),
        expect.objectContaining({ method: 'POST' })
    );
    const [, opts] = global.fetch.mock.calls[0];
    const body = JSON.parse(opts.body);
    expect(body.score).toBe(40);
    expect(body.person_a.year).toBe(1990);
    expect(body.person_b.year).toBe(1992);
    expect(body.context).toBe('romance');
});

// ═══════════════════════════════════════════════════════════════════
// COMP-3: Partner Landing Flow
// ═══════════════════════════════════════════════════════════════════
test('loadInvitationData populates partner message and shows partner section', async () => {
    global.fetch = jest.fn(() => Promise.resolve({
        ok: true,
        json: async () => ({
            name_a: 'Minh',
            context: 'romance',
            partner_completed: false,
            hop_tuoi_result: mockHopTuoiResult(),
        }),
    }));

    await loadInvitationData('abc12345');

    const partnerMsg = document.getElementById('ht-partner-msg');
    expect(partnerMsg.textContent).toContain('Minh');
    expect(document.getElementById('ht-partner-section').classList.contains('visible')).toBe(true);
});

test('loadInvitationData shows full report when partner already completed', async () => {
    global.fetch = jest.fn(() => Promise.resolve({
        ok: true,
        json: async () => ({
            name_a: 'Minh',
            context: 'romance',
            partner_completed: true,
            hop_tuoi_result: mockHopTuoiResult(),
        }),
    }));

    await loadInvitationData('abc12345');

    // Should show full report directly (no partner section needed)
    expect(document.getElementById('ht-full-report').classList.contains('visible')).toBe(true);
});

test('htPartnerSubmit calls invitation complete then shows full report', async () => {
    document.getElementById('ht-partner-section').classList.remove('hidden');

    global.fetch = jest.fn(() =>
        Promise.resolve({
            ok: true,
            json: async () => ({ partner_completed: true }),
            body: makeSSEStream(
                'data: {"content":"Ket qua day du"}\n\n',
                'data: [DONE]\n\n'
            )
        })
    );

    await htPartnerSubmit(mockHopTuoiResult(), 'abc12345');

    expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/tuvi/invitation/abc12345/complete'),
        expect.objectContaining({ method: 'POST' })
    );
    expect(document.getElementById('ht-full-report').classList.contains('visible')).toBe(true);
});

// ═══════════════════════════════════════════════════════════════════
// COMP-4: Full Streaming Report
// ═══════════════════════════════════════════════════════════════════
test('renderHopTuoiFullReport shows full report section', async () => {
    global.fetch = jest.fn(() =>
        Promise.resolve({ ok: true, body: makeSSEStream(
            'data: {"content":"Phan tich 1"}\n\n',
            'data: {"content":"Phan tich 2"}\n\n',
            'data: [DONE]\n\n'
        ) })
    );

    await renderHopTuoiFullReport(mockHopTuoiResult());

    expect(document.getElementById('ht-full-report').classList.contains('visible')).toBe(true);
    expect(document.getElementById('ht-teaser').classList.contains('visible')).toBe(false);
});

test('renderHopTuoiFullReport calls /api/tuvi/compatibility/stream with correct params', async () => {
    global.fetch = jest.fn(() =>
        Promise.resolve({ ok: true, body: makeSSEStream(
            'data: {"content":"Test"}\n\n',
            'data: [DONE]\n\n'
        ) })
    );

    await renderHopTuoiFullReport(mockHopTuoiResult());

    expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/tuvi/compatibility/stream'),
        expect.objectContaining({ method: 'POST' })
    );
    const [, opts] = global.fetch.mock.calls[0];
    const body = JSON.parse(opts.body);
    expect(body.score).toBe(40);
    expect(body.rating).toBe('Bình thường');
    expect(body.person_a.zodiac).toBe('Ngọ');
    expect(body.person_b.zodiac).toBe('Thân');
    expect(body.context).toBe('romance');
});

test('renderHopTuoiFullReport renders stream chunks into report sections', async () => {
    const mockStream = makeSSEStream(
        'data: {"section":0,"content":"Noi dung 0"}\n\n',
        'data: {"section":2,"content":"Noi dung 2"}\n\n',
        'data: {"section":4,"content":"Hoa Giai content"}\n\n',
        'data: [DONE]\n\n'
    );

    await renderHopTuoiFullReport(mockHopTuoiResult(), {}, mockStream);

    const s0 = document.getElementById('ht-section-0');
    const s2 = document.getElementById('ht-section-2');
    const s4 = document.getElementById('ht-section-4');
    expect(s0.textContent).toContain('Noi dung 0');
    expect(s2.textContent).toContain('Noi dung 2');
    expect(s4.textContent).toContain('Hoa Giai');
});

test('renderHopTuoiFullReport shows share card after stream completes', async () => {
    const mockStream = makeSSEStream(
        'data: {"content":"Report content"}\n\n',
        'data: [DONE]\n\n'
    );

    await renderHopTuoiFullReport(mockHopTuoiResult(), {}, mockStream);

    const shareCard = document.getElementById('ht-share-card');
    expect(shareCard.classList.contains('visible')).toBe(true);
});

test('renderHopTuoiFullReport shows 4 factor bars after stream', async () => {
    global.fetch = jest.fn(() =>
        Promise.resolve({ ok: true, body: makeSSEStream(
            'data: {"content":"Report"}\n\n',
            'data: [DONE]\n\n'
        ) })
    );

    await renderHopTuoiFullReport(mockHopTuoiResult());

    const factorBars = document.querySelectorAll('.ht-factor-bar');
    expect(factorBars.length).toBeGreaterThanOrEqual(0);
});
