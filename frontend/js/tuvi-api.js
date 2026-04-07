/**
 * Tử Vi API - Client for Tử Vi chart API
 */

const API_BASE = (window.location.pathname.replace(/\/$/, '') || '');

async function fetchTuviChart(data) {
    const response = await fetch(`${API_BASE}/api/tuvi/chart`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Lỗi khi gọi API');
    }

    return response.json();
}

function formatLunarDate(lunar) {
    return `Ngày ${lunar.day} tháng ${lunar.month} năm ${lunar.year}${lunar.is_leap ? ' (nhuận)' : ''}`;
}

function formatSolarDate(solar) {
    return `${solar.day}/${solar.month}/${solar.year}`;
}

function formatTime(hour, minute) {
    return `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
}

const tuviApi = {
    async getChart(year, month, day, hour, minute, is_leap_month, gender, nam_xem) {
        return fetchTuviChart({ year, month, day, hour, minute, is_leap_month, gender, nam_xem });
    }
};

// Profile functions
const TV_API_BASE = (window.location.pathname.replace(/\/$/, '') || '');


let profileGender = 'male';
let profileInterests = [];

function openProfileModal() {
    const modal = document.getElementById('profile-modal');
    if (modal) modal.style.display = 'flex';
    loadProfile();
}

function closeProfileModal() {
    const modal = document.getElementById('profile-modal');
    if (modal) modal.style.display = 'none';
}

async function loadProfile() {
    try {
        const deviceId = getDeviceId('tuvi_device_id');
        const response = await fetch(`${TV_API_BASE}/api/profile?device_id=${encodeURIComponent(deviceId)}`);
        const data = await response.json();
        const profile = data.profile;

        if (profile && profile.name) {
            document.getElementById('profile-name').value = profile.name || '';
            document.getElementById('profile-birth-date').value = profile.birth_date || '';
            selectProfileGender(profile.gender || 'male');
            const interests = profile.interests || [];
            profileInterests = interests;
            document.querySelectorAll('.interest-chip').forEach(chip => {
                chip.classList.toggle('active', interests.includes(chip.dataset.interest));
            });
            localStorage.setItem('tuvi_profile', JSON.stringify(profile));
        }
    } catch (error) {
        console.error('Failed to load profile:', error);
    }
}

function selectProfileGender(gender) {
    profileGender = gender;
    document.querySelectorAll('.profile-gender-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.gender === gender);
    });
}

function toggleInterest(interest) {
    const idx = profileInterests.indexOf(interest);
    if (idx > -1) {
        profileInterests.splice(idx, 1);
    } else {
        profileInterests.push(interest);
    }
    document.querySelectorAll('.interest-chip').forEach(chip => {
        chip.classList.toggle('active', profileInterests.includes(chip.dataset.interest));
    });
}

async function saveProfile() {
    try {
        const deviceId = getDeviceId('tuvi_device_id');
        const name = document.getElementById('profile-name').value;
        const birthDate = document.getElementById('profile-birth-date').value;

        const response = await fetch(`${TV_API_BASE}/api/profile?device_id=${encodeURIComponent(deviceId)}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                device_id: deviceId,
                name: name,
                birth_date: birthDate,
                gender: profileGender,
                interests: profileInterests
            })
        });

        const data = await response.json();
        localStorage.setItem('tuvi_profile', JSON.stringify(data));
        alert('Đã lưu hồ sơ!');
        closeProfileModal();
    } catch (error) {
        console.error('Failed to save profile:', error);
        alert('Có lỗi khi lưu hồ sơ.');
    }
}

async function deleteProfile() {
    if (!confirm('Bạn có chắc muốn xóa hồ sơ?')) return;
    try {
        const deviceId = getDeviceId('tuvi_device_id');
        await fetch(`${TV_API_BASE}/api/profile?device_id=${encodeURIComponent(deviceId)}`, { method: 'DELETE' });
        localStorage.removeItem('tuvi_profile');
        document.getElementById('profile-name').value = '';
        document.getElementById('profile-birth-date').value = '';
        selectProfileGender('male');
        profileInterests = [];
        document.querySelectorAll('.interest-chip').forEach(chip => chip.classList.remove('active'));
        alert('Đã xóa hồ sơ!');
        closeProfileModal();
    } catch (error) {
        console.error('Failed to delete profile:', error);
    }
}

// BDG-1: fetch badges for Tu Vi
async function fetchAndRenderBadges() {
    try {
        const deviceId = typeof getDeviceId === 'function' ? getDeviceId() : null;
        if (!deviceId) return;
        const res = await fetch(`${API_BASE}/api/badges?device_id=` + encodeURIComponent(deviceId));
        if (!res.ok) return;
        const data = await res.json();
        if (typeof renderBadgeShelf === 'function') {
            renderBadgeShelf('badge-shelf', data.badges || [], data.cross_badges || []);
            const shelf = document.getElementById('badge-shelf');
            if (shelf) shelf.classList.remove('hidden');
        }
    } catch (e) { console.warn('fetchBadges failed:', e); }
}

fetchAndRenderBadges();
