/**
 * hop-tuoi.js — COMP-2: Tu Vi Hợp Tuổi Entry Form + Teaser Result
 * Standalone page at /hop-tuoi on TV app (port 17070).
 * Uses birth-year-only Nap Am + zodiac lookup (no iztro-py required for teaser).
 */

// ── State ──────────────────────────────────────────────────────────
const API_BASE = (window.location.pathname.replace(/\/[^/]*$/, '') || '');
let _htSelectedContext = 'romance';
let _htCurrentResult = null;
let _htInvitationId = null;
let _htDeviceId = '';

// ── Init ──────────────────────────────────────────────────────────
(function init() {
    // Seed device ID
    if (typeof getDeviceId === 'function') {
        _htDeviceId = getDeviceId('tuvi_device_id');
    }

    // Check for deep link invite param
    const params = new URLSearchParams(window.location.search);
    const inviteId = params.get('invite');
    if (inviteId) {
        _htInvitationId = inviteId;
        loadInvitationData(inviteId);
    }

    // Bind context selector
    document.querySelectorAll('.ht-context-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            htSelectContext(btn.dataset.context);
        });
    });

    // Bind skip link
    const skipLink = document.getElementById('ht-skip-link');
    if (skipLink) {
        skipLink.addEventListener('click', e => {
            htSkipGate(e);
        });
    }
})();

// ── Context Selector ───────────────────────────────────────────────
function htSelectContext(context) {
    _htSelectedContext = context;
    document.querySelectorAll('.ht-context-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.context === context);
    });
}

// ── Form Submit ────────────────────────────────────────────────────
async function htSubmit() {
    const yearA = parseInt(document.getElementById('ht-a-year')?.value);
    const yearB = parseInt(document.getElementById('ht-b-year')?.value);

    // Validate range
    const minYear = 1940;
    const maxYear = 2015;
    let hasError = false;

    if (!yearA || yearA < minYear || yearA > maxYear) {
        const errEl = document.getElementById('ht-a-error');
        if (errEl) {
            errEl.textContent = `Năm sinh phải từ ${minYear} đến ${maxYear}`;
            errEl.classList.add('visible');
        }
        hasError = true;
    } else {
        document.getElementById('ht-a-error')?.classList.remove('visible');
    }

    if (!yearB || yearB < minYear || yearB > maxYear) {
        const errEl = document.getElementById('ht-b-error');
        if (errEl) {
            errEl.textContent = `Năm sinh phải từ ${minYear} đến ${maxYear}`;
            errEl.classList.add('visible');
        }
        hasError = true;
    } else {
        document.getElementById('ht-b-error')?.classList.remove('visible');
    }

    if (hasError) return;

    const loading = document.getElementById('ht-loading');
    const errorEl = document.getElementById('ht-error');
    if (loading) loading.classList.add('visible');
    if (errorEl) {
        errorEl.classList.remove('visible');
        errorEl.textContent = '';
    }

    try {
        const deviceId = _htDeviceId || (typeof getDeviceId === 'function' ? getDeviceId('tuvi_device_id') : '');
        const res = await fetch(`${API_BASE}/api/tuvi/hop-tuoi`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                year_a: yearA,
                year_b: yearB,
                context: _htSelectedContext,
                device_id: deviceId,
            }),
        });

        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            throw new Error(data.detail || `HTTP ${res.status}`);
        }

        const data = await res.json();
        _htCurrentResult = data;

        if (loading) loading.classList.remove('visible');

        // ANA-1: track compatibility_check funnel event
        if (typeof trackEvent === 'function') {
            trackEvent('tuvi', 'compatibility_check', {
                method: 'tv',
                context: _htSelectedContext,
                zodiac_a: data.person_a ? data.person_a.zodiac : '',
                zodiac_b: data.person_b ? data.person_b.zodiac : '',
                element_a: data.person_a ? data.person_a.element : '',
                element_b: data.person_b ? data.person_b.element : '',
                score: data.combined_score !== undefined ? data.combined_score : (data.score || 0),
                rating: data.combined_rating || data.rating || '',
            });
        }

        renderHopTuoiTeaser(data);
    } catch (e) {
        if (loading) loading.classList.remove('visible');
        if (errorEl) {
            errorEl.textContent = 'Lỗi: ' + e.message;
            errorEl.classList.add('visible');
        }
    }
}

// ── Teaser Render ─────────────────────────────────────────────────
function renderHopTuoiTeaser(data) {
    const teaser = document.getElementById('ht-teaser');
    if (teaser) teaser.classList.add('visible');

    // Zodiac pair
    const zodiacA = document.getElementById('ht-zodiac-a');
    const zodiacB = document.getElementById('ht-zodiac-b');
    if (zodiacA) zodiacA.textContent = data.person_a.zodiac;
    if (zodiacB) zodiacB.textContent = data.person_b.zodiac;

    // Zodiac verdict badge
    const badge = document.getElementById('ht-zodiac-verdict-badge');
    if (badge) badge.textContent = data.zodiac_verdict.label;

    // Element arrow
    const arrow = document.getElementById('ht-element-arrow');
    if (arrow) {
        arrow.textContent = `${data.person_a.element} → ${data.person_b.element}  ${data.element_verdict.label}`;
    }

    // Score circle
    const scoreVal = document.getElementById('ht-score-value');
    if (scoreVal) scoreVal.textContent = String(data.combined_score);

    const rating = document.getElementById('ht-score-rating');
    if (rating) rating.textContent = data.combined_rating;

    // Summary
    const summary = document.getElementById('ht-summary');
    if (summary) summary.textContent = data.summary;

    // Hide loading
    document.getElementById('ht-loading')?.classList.remove('visible');
}

// ── Invitation Modal ──────────────────────────────────────────────
async function htOpenInvitationModal() {
    if (!_htCurrentResult) return;

    const modal = document.getElementById('ht-invite-modal');
    if (modal) modal.classList.add('visible');

    try {
        const deviceId = _htDeviceId || (typeof getDeviceId === 'function' ? getDeviceId('tuvi_device_id') : '');
        const nameA = document.getElementById('ht-a-name')?.value || '';
        const nameB = document.getElementById('ht-b-name')?.value || '';
        const res = await fetch(`${API_BASE}/api/tuvi/invitation/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                initiator_device_id: deviceId,
                year_a: _htCurrentResult.person_a.year,
                year_b: _htCurrentResult.person_b.year,
                name_a: nameA,
                name_b: nameB,
                context: _htSelectedContext,
                hop_tuoi_result: _htCurrentResult,
            }),
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        _htInvitationId = data.invitation_id;

        const messageEl = document.getElementById('ht-invite-message');
        // ANA-3: use message_text from BE (A/B variant), not deep_link
        if (messageEl) messageEl.value = data.message_text || data.deep_link || '';

        const headerEl = document.getElementById('ht-invite-header');
        if (headerEl) headerEl.textContent = 'Mời người kia cùng xem để mở khóa phân tích đầy đủ';
    } catch (e) {
        console.error('Invitation create failed:', e);
    }
}

function htCloseInviteModal() {
    const modal = document.getElementById('ht-invite-modal');
    if (modal) modal.classList.remove('visible');
}

// ── Partner Landing — Load Invitation ─────────────────────────────
async function loadInvitationData(inviteId) {
    // ANA-1: track invitation_clicked funnel event
    if (typeof trackEvent === 'function') trackEvent('tuvi', 'invitation_clicked', { invitation_id: inviteId, method: 'tv' });

    try {
        const res = await fetch(`${API_BASE}/api/tuvi/invitation/${inviteId}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        _htInvitationId = inviteId;

        // If partner already completed, show full report directly
        if (data.partner_completed && data.hop_tuoi_result) {
            _htCurrentResult = data.hop_tuoi_result;
            await renderHopTuoiFullReport(data.hop_tuoi_result, { invitation_id: inviteId });
            return;
        }

        // Show partner greeting + teaser
        if (data.name_a) {
            const msgEl = document.getElementById('ht-partner-msg');
            if (msgEl) msgEl.textContent = `${data.name_a} đã xem tương hợp với bạn`;
            const partnerSection = document.getElementById('ht-partner-section');
            if (partnerSection) partnerSection.classList.add('visible');
        }

        if (data.hop_tuoi_result) {
            _htCurrentResult = data.hop_tuoi_result;
            renderHopTuoiTeaser(data.hop_tuoi_result);
        }

        if (data.context) {
            htSelectContext(data.context);
        }
    } catch (e) {
        console.error('Failed to load invitation:', e);
    }
}

// ── Deep Link Share ───────────────────────────────────────────────
function htCopyLink() {
    const inviteId = _htInvitationId || '';
    if (typeof trackEvent === 'function') trackEvent('tuvi', 'invitation_sent', { channel: 'copy', invitation_id: inviteId, method: 'tv' });
    const link = document.getElementById('ht-invite-message')?.value || '';
    if (navigator.clipboard) {
        navigator.clipboard.writeText(link).then(() => {
            alert('Đã copy link!');
        }).catch(() => {
            alert('Không thể copy');
        });
    }
}

function htShareZalo() {
    const inviteId = _htInvitationId || '';
    if (typeof trackEvent === 'function') trackEvent('tuvi', 'invitation_sent', { channel: 'zalo', invitation_id: inviteId, method: 'tv' });
    const link = document.getElementById('ht-invite-message')?.value || '';
    const encoded = encodeURIComponent(link);
    window.open(`https://zalo.me/share?url=${encoded}`, '_blank');
}

function htShareMessenger() {
    const inviteId = _htInvitationId || '';
    if (typeof trackEvent === 'function') trackEvent('tuvi', 'invitation_sent', { channel: 'messenger', invitation_id: inviteId, method: 'tv' });
    const link = document.getElementById('ht-invite-message')?.value || '';
    const encoded = encodeURIComponent(link);
    window.open(`https://www.facebook.com/v21.0/dialog/send?link=${encoded}&redirect_uri=${encoded}`, '_blank');
}

// ── Skip Gate ────────────────────────────────────────────────────
async function htSkipGate(event, data) {
    if (event) event.preventDefault();
    htCloseInviteModal();
    await renderHopTuoiFullReport(data || _htCurrentResult, { skipped: true });
}

// ── Partner Landing — Submit Partner Data ─────────────────────────
async function htPartnerSubmit(data, invitationId) {
    const result = data || _htCurrentResult;
    const invId = invitationId || _htInvitationId;
    if (!invId || !result) return;
    try {
        const deviceId = _htDeviceId || (typeof getDeviceId === 'function' ? getDeviceId('tuvi_device_id') : '');
        const res = await fetch(`${API_BASE}/api/tuvi/invitation/${invId}/complete`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ partner_device_id: deviceId }),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const resp = await res.json();
        if (resp.partner_completed) {
            document.getElementById('ht-partner-section')?.classList.remove('visible');
            await renderHopTuoiFullReport(result, { invitation_id: invId });
        }
    } catch (e) {
        console.error('Partner submit failed:', e);
    }
}

// ── Full Streaming Report (COMP-4) ───────────────────────────────
async function renderHopTuoiFullReport(data, opts = {}, streamOverride) {
    const fullReport = document.getElementById('ht-full-report');
    const teaser = document.getElementById('ht-teaser');
    if (teaser) teaser.classList.remove('visible');
    if (fullReport) fullReport.classList.add('visible');

    // Clear previous sections
    for (let i = 0; i < 5; i++) {
        const el = document.getElementById(`ht-section-${i}`);
        if (el) el.textContent = '';
    }

    try {
        let reader;
        if (streamOverride) {
            reader = streamOverride.getReader();
        } else {
            const deviceId = _htDeviceId || (typeof getDeviceId === 'function' ? getDeviceId('tuvi_device_id') : '');
            const params = {
                score: data.combined_score,
                rating: data.combined_rating,
                factors: {
                    zodiac: data.zodiac_verdict,
                    element: data.element_verdict,
                },
                person_a: data.person_a,
                person_b: data.person_b,
                device_id: deviceId,
                context: _htSelectedContext,
                invitation_id: opts.invitation_id || _htInvitationId || null,
            };

            const res = await fetch(`${API_BASE}/api/tuvi/compatibility/stream`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(params),
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            reader = res.body.getReader();
        }

        const decoder = new TextDecoder();
        let currentSection = 0;
        let buffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });
            // Split by \n\n to get complete SSE events
            const events = buffer.split('\n\n');
            buffer = events.pop() || '';

            for (const event of events) {
                const line = event.trim();
                if (!line || !line.startsWith('data: ')) continue;
                const raw = line.slice(6).trim();
                if (raw === '[DONE]') {
                    // ANA-1: track full_report_viewed funnel event
                    if (typeof trackEvent === 'function') {
                        trackEvent('tuvi', 'full_report_viewed', {
                            invitation_id: opts.invitation_id || _htInvitationId || null,
                            method: 'tv',
                            skipped: opts.skipped || false,
                        });
                    }
                    const shareCard = document.getElementById('ht-share-card');
                    if (shareCard) {
                        shareCard.classList.add('visible');
                        // ANA-1: track share_card_generated
                        if (typeof trackEvent === 'function') {
                            trackEvent('tuvi', 'share_card_generated', {
                                method: 'tv',
                                score: data.combined_score || 0,
                                zodiac_pair: (data.person_a?.zodiac || '') + '+' + (data.person_b?.zodiac || ''),
                            });
                        }
                    }
                    return;
                }
                try {
                    const chunk = JSON.parse(raw);
                    if (chunk.section !== undefined) currentSection = chunk.section;
                    if (chunk.content) {
                        const el = document.getElementById(`ht-section-${currentSection}`);
                        if (el) el.textContent += chunk.content;
                    }
                } catch {
                    const el = document.getElementById(`ht-section-${currentSection}`);
                    if (el) el.textContent += raw;
                }
            }
        }

        const shareCard = document.getElementById('ht-share-card');
        if (shareCard) {
            shareCard.classList.add('visible');
            // ANA-1: track share_card_generated (fallback path)
            if (typeof trackEvent === 'function') {
                trackEvent('tuvi', 'share_card_generated', {
                    method: 'tv',
                    score: data.combined_score || 0,
                    zodiac_pair: (data.person_a?.zodiac || '') + '+' + (data.person_b?.zodiac || ''),
                });
            }
        }
    } catch (e) {
        console.error('Full report stream failed:', e);
    }
}

// ── CommonJS export ─────────────────────────────────────────────
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
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
    };
}
