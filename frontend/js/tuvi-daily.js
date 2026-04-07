// Tử Vi — Daily Fortune (TV-FP-1), History Sidebar (TV-FP-4), Push Opt-in (TV-FP-3)

const TV_HISTORY_KEY  = 'tuvi_history';
const TV_DAILY_EXP_KEY = 'tuvi_daily_expanded';
const TV_PUSH_KEY     = 'tuvi_push_subscribed';
const TV_CHART_COUNT  = 'tuvi_chart_count';
const TV_VAPID_KEY    = 'BEl62iUYgUivxIkv69yViEuiBIa40Hi37K6MoRCkrHMOJAP3kHn6aHWCxnONbz5yC2dLIiHGSGxb8D4bvWkDyE';
var _apiBase = (window.location.pathname.replace(/\/$/, '') || '');

// =========================================
// TV-FP-1: DAILY FORTUNE
// =========================================

async function loadDailyFortune() {
    const card = document.getElementById('daily-fortune-card');
    if (!card) return;

    const deviceId = getDeviceId();
    const expandKey = localStorage.getItem(TV_DAILY_EXP_KEY);
    // First visit: expand; subsequent: collapsed
    const shouldExpand = expandKey === null;
    if (!shouldExpand) {
        card.classList.add('collapsed');
        document.getElementById('daily-chevron').textContent = '▼';
    }

    const body = document.getElementById('daily-fortune-body');
    body.innerHTML = '<div class="daily-loading"><span></span><span></span><span></span></div>';

    try {
        const res = await fetch(`${_apiBase}/api/tuvi/daily?device_id=${encodeURIComponent(deviceId)}`);
        const data = await res.json();

        if (data.error === 'no_profile') {
            body.innerHTML = `
                <p class="daily-noprofile">
                    Nhập ngày sinh để xem vận hạn hôm nay
                    <button class="daily-noprofile-link" onclick="openProfileModal()">→ Mở hồ sơ</button>
                </p>
            `;
            return;
        }

        // Streak badge
        const streak = data.streak_count || 0;
        document.getElementById('daily-streak').textContent = `🔥 ${streak} ngày`;
        document.getElementById('daily-streak').classList.remove('hidden');

        // Palace label
        if (data.palace_name) {
            document.getElementById('daily-palace').textContent = `Cung: ${data.palace_name}`;
            document.getElementById('daily-palace').classList.remove('hidden');
        }

        // Fortune text
        body.innerHTML = `<div class="daily-text">${(data.fortune_text || '').replace(/\n/g, '<br>')}</div>`;

        // Mark as visited so future loads start collapsed
        if (expandKey === null) {
            localStorage.setItem(TV_DAILY_EXP_KEY, '1');
        }

    } catch {
        body.innerHTML = '<p class="daily-error">Không thể tải vận hạn hôm nay</p>';
    }
}

function toggleDailyCard() {
    const card = document.getElementById('daily-fortune-card');
    const chevron = document.getElementById('daily-chevron');
    if (!card) return;
    const isCollapsed = card.classList.toggle('collapsed');
    chevron.textContent = isCollapsed ? '▼' : '▲';
}

// =========================================
// TV-FP-4: HISTORY SIDEBAR
// =========================================

function getTuviHistory() {
    try {
        return JSON.parse(localStorage.getItem(TV_HISTORY_KEY) || '[]');
    } catch { return []; }
}

function saveTuviHistory(params, chartData) {
    const history = getTuviHistory();
    const entry = {
        id: Date.now(),
        day:    params.day,
        month:  params.month,
        year:   params.year,
        hour:   params.hour,
        minute: params.minute || 0,
        gender: params.gender,
        menhCung: chartData?.cung_menh || '',
        napAm:    chartData?.nap_am   || '',
        label:  `${params.day}/${params.month}/${params.year}`,
        timestamp: Date.now()
    };
    // Avoid duplicate (same date+hour+gender)
    const dupe = history.findIndex(h =>
        h.day === entry.day && h.month === entry.month &&
        h.year === entry.year && h.hour === entry.hour && h.gender === entry.gender
    );
    if (dupe > -1) history.splice(dupe, 1);
    history.unshift(entry);
    if (history.length > 10) history.pop();
    localStorage.setItem(TV_HISTORY_KEY, JSON.stringify(history));
    renderHistorySidebar();
    return entry;
}

function renderHistorySidebar() {
    const list = document.getElementById('tv-history-list');
    if (!list) return;
    const history = getTuviHistory();

    if (!history.length) {
        list.innerHTML = '<li class="tv-history-empty">' + t('common.history_empty') + '</li>';
        return;
    }

    list.innerHTML = history.map(entry => `
        <li class="tv-history-item" onclick="reloadChart(${entry.id})">
            <div class="tv-history-label">${entry.label}</div>
            <div class="tv-history-meta">
                ${entry.menhCung ? `<span class="tv-history-menh">${entry.menhCung}</span>` : ''}
                <span class="tv-history-gender">${entry.gender === 'nam' ? '☉ Nam' : '☽ Nữ'}</span>
            </div>
        </li>
    `).join('');
}

async function reloadChart(entryId) {
    const history = getTuviHistory();
    const entry = history.find(h => h.id === entryId);
    if (!entry) return;

    // Fill form inputs
    document.getElementById('day').value   = entry.day;
    document.getElementById('month').value = entry.month;
    document.getElementById('year').value  = entry.year;
    document.getElementById('hour').value  = entry.hour;

    // Set Địa Chi button selection
    document.querySelectorAll('.diachi-hour-btn').forEach(btn => {
        btn.classList.toggle('selected', parseInt(btn.dataset.hour) === entry.hour);
    });

    // Set gender pills
    const isMale = entry.gender === 'nam';
    document.getElementById('pill-nam').classList.toggle('selected', isMale);
    document.getElementById('pill-nu').classList.toggle('selected', !isMale);
    document.getElementById('gender-nam').checked = isMale;
    document.getElementById('gender-nu').checked  = !isMale;

    closeSidebar();

    // Submit the form
    try {
        showLoading();
        const data = await tuviApi.getChart(
            entry.year, entry.month, entry.day,
            entry.hour, entry.minute, false, entry.gender
        );
        renderChart(data);
    } catch (error) {
        showError(error.message);
    }
}

function clearTuviHistory() {
    if (!confirm('Xóa toàn bộ lịch sử?')) return;
    localStorage.removeItem(TV_HISTORY_KEY);
    renderHistorySidebar();
}

function toggleSidebar() {
    const sidebar = document.getElementById('tv-sidebar');
    const overlay = document.getElementById('tv-sidebar-overlay');
    sidebar.classList.toggle('open');
    overlay.classList.toggle('open');
}

function closeSidebar() {
    document.getElementById('tv-sidebar').classList.remove('open');
    document.getElementById('tv-sidebar-overlay').classList.remove('open');
}

// =========================================
// TV-FP-2: SHARE AS IMAGE
// =========================================

let tuviShareImageData = null;

async function shareTuviChart() {
    if (!currentTuviData) {
        alert(t('tv.error_view_chart_first'));
        return;
    }

    const btn = document.querySelector('.btn-share-chart');
    if (btn) btn.textContent = '⏳ Đang tạo...';

    try {
        const response = await fetch(`${_apiBase}/api/tuvi/share`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chart_data: currentTuviData,
                device_id: getDeviceId()
            })
        });

        if (!response.ok) throw new Error('Share API error');
        const data = await response.json();

        // Prefer story (vertical) image for sharing
        const imageUrl = data.story || data.card;
        tuviShareImageData = imageUrl;

        const preview = document.getElementById('tuvi-share-preview');
        if (preview) {
            preview.innerHTML = `<img src="${imageUrl}" alt="Lá số Tử Vi" style="max-width:100%;border-radius:8px;">`;
        }

        const modal = document.getElementById('tuvi-share-modal');
        if (modal) modal.style.display = 'flex';

        const nativeBtn = document.getElementById('btn-tuvi-share-native');
        if (nativeBtn) {
            nativeBtn.style.display = (navigator.share && navigator.canShare) ? 'flex' : 'none';
        }

    } catch (e) {
        console.error('Share error:', e);
        alert('Không thể tạo hình ảnh chia sẻ');
    } finally {
        if (btn) btn.textContent = '✦ Chia sẻ lá số';
    }
}

function closeTuviShareModal() {
    const modal = document.getElementById('tuvi-share-modal');
    if (modal) modal.style.display = 'none';
    tuviShareImageData = null;
}

async function shareTuviNative() {
    if (!tuviShareImageData) return;
    try {
        const blob = await fetch(tuviShareImageData).then(r => r.blob());
        const file = new File([blob], 'tuvi-la-so.png', { type: 'image/png' });
        await navigator.share({ files: [file], title: 'Lá Số Tử Vi', text: 'Xem lá số tử vi của tôi' });
        closeTuviShareModal();
    } catch (e) {
        if (e.name !== 'AbortError') downloadTuviImage();
    }
}

function downloadTuviImage() {
    if (!tuviShareImageData) return;
    const link = document.createElement('a');
    link.download = 'tuvi-la-so.png';
    link.href = tuviShareImageData;
    link.click();
    closeTuviShareModal();
}

// =========================================
// TV-FP-3: PUSH OPT-IN
// =========================================

async function registerTuviSW() {
    if (!('serviceWorker' in navigator)) return;
    try {
        await navigator.serviceWorker.register(`${_apiBase}/sw.js`, { scope: `${_apiBase}/` });
    } catch (e) {
        console.warn('SW registration failed:', e);
    }
}

function showPushOptIn() {
    if (localStorage.getItem(TV_PUSH_KEY) === 'granted') return;
    if (localStorage.getItem(TV_PUSH_KEY) === 'dismissed') return;
    const banner = document.getElementById('push-optin-banner');
    if (banner) banner.classList.remove('hidden');
}

async function subscribePush() {
    const banner = document.getElementById('push-optin-banner');
    if (banner) banner.classList.add('hidden');
    localStorage.setItem(TV_PUSH_KEY, 'granted');

    try {
        const reg = await navigator.serviceWorker.ready;
        const sub = await reg.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(TV_VAPID_KEY)
        });
        await fetch(`${_apiBase}/api/push/subscribe`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ subscription: sub, app: 'tuvi', device_id: getDeviceId() })
        });
    } catch (e) {
        console.warn('Push subscribe failed:', e);
    }
}

function dismissPush() {
    localStorage.setItem(TV_PUSH_KEY, 'dismissed');
    const banner = document.getElementById('push-optin-banner');
    if (banner) banner.classList.add('hidden');
}

function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
    const rawData = atob(base64);
    const output = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; i++) output[i] = rawData.charCodeAt(i);
    return output;
}

// =========================================
// INIT
// =========================================
document.addEventListener('DOMContentLoaded', () => {
    registerTuviSW();
    loadDailyFortune();
});

window.addEventListener('i18n:ready', () => {
    renderHistorySidebar();
});

// CommonJS export for Jest tests (no-op in browser)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loadDailyFortune, toggleDailyCard,
        getTuviHistory, saveTuviHistory, renderHistorySidebar,
        clearTuviHistory, reloadChart, toggleSidebar, closeSidebar,
        shareTuviChart, closeTuviShareModal, downloadTuviImage,
        showPushOptIn, dismissPush, subscribePush,
        urlBase64ToUint8Array, TV_HISTORY_KEY, TV_PUSH_KEY, TV_DAILY_EXP_KEY
    };
}
