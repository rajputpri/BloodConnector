/* ============================================================
   BloodConnect — Real-time Notification Client
   SignalR + Web Audio API + Toast
   ============================================================ */
(function () {
    'use strict';

    const HUB_URL = '/hubs/notifications';

    // ==================== SOUND (Web Audio API) ====================
    let audioCtx = null;
    let soundEnabled = localStorage.getItem('bc-sound') !== 'off';

    function ensureAudioContext() {
        if (!audioCtx) {
            try {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            } catch (e) {
                console.warn('[Notif] Audio not supported');
                return null;
            }
        }
        if (audioCtx.state === 'suspended') {
            audioCtx.resume().catch(() => {});
        }
        return audioCtx;
    }

    function playNotificationSound() {
        if (!soundEnabled) return;
        const ctx = ensureAudioContext();
        if (!ctx) return;

        const now = ctx.currentTime;

        function playTone(freq, startTime, duration, volume) {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.type = 'sine';
            osc.frequency.value = freq;

            gain.gain.setValueAtTime(0, startTime);
            gain.gain.linearRampToValueAtTime(volume, startTime + 0.015);
            gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration);

            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(startTime);
            osc.stop(startTime + duration);
        }

        // WhatsApp-style two-tone chime
        playTone(880, now, 0.20, 0.22);           // A5
        playTone(1174.66, now + 0.13, 0.35, 0.20); // D6
    }

    // ==================== TOAST ====================
    function escapeHtml(s) {
        const d = document.createElement('div');
        d.textContent = s == null ? '' : String(s);
        return d.innerHTML;
    }

    function showNotificationToast(payload) {
        const existing = document.getElementById('bc-notif-toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.id = 'bc-notif-toast';
        toast.className = 'bc-notif-toast';

        const icon =
            payload.type === 'request' ? '🩸' :
            payload.type === 'message' ? '✉' :
            payload.type === 'offer' ? '🤝' :
            payload.type === 'offer-status' ? '✓' : '🔔';

        toast.innerHTML =
            '<div class="bc-notif-toast-icon">' + icon + '</div>' +
            '<div class="bc-notif-toast-body">' +
            '  <div class="bc-notif-toast-title">' + escapeHtml(payload.title || 'Notification') + '</div>' +
            '  <div class="bc-notif-toast-msg">' + escapeHtml(payload.message || '') + '</div>' +
            '</div>' +
            '<button class="bc-notif-toast-close" aria-label="Close">×</button>';

        document.body.appendChild(toast);

        requestAnimationFrame(() => toast.classList.add('is-visible'));

        toast.addEventListener('click', function (e) {
            if (e.target.classList.contains('bc-notif-toast-close')) return;
            if (payload.url) window.location.href = payload.url;
        });

        toast.querySelector('.bc-notif-toast-close').addEventListener('click', function (e) {
            e.stopPropagation();
            hideToast(toast);
        });

        setTimeout(() => hideToast(toast), 7000);
    }

    function hideToast(toast) {
        if (!toast.parentNode) return;
        toast.classList.remove('is-visible');
        setTimeout(() => { if (toast.parentNode) toast.remove(); }, 400);
    }

    // ==================== BELL BADGE ====================
    function incrementBellBadge() {
        const btn = document.querySelector('.bc-bell-btn');
        if (!btn) return;

        let badge = btn.querySelector('.bc-bell-badge');
        if (!badge) {
            badge = document.createElement('span');
            badge.className = 'bc-bell-badge';
            badge.textContent = '1';
            btn.appendChild(badge);
        } else {
            const current = parseInt(String(badge.textContent).replace('+', ''), 10) || 0;
            const next = current + 1;
            badge.textContent = next > 99 ? '99+' : String(next);
        }

        badge.classList.remove('is-pulsing');
        void badge.offsetWidth;
        badge.classList.add('is-pulsing');

        btn.classList.remove('is-ringing');
        void btn.offsetWidth;
        btn.classList.add('is-ringing');
    }

    function prependNotificationItem(payload) {
        const list = document.querySelector('.bc-bell-list');
        const empty = document.querySelector('.bc-bell-empty');

        if (empty) empty.remove();
        if (!list) return;

        const icon =
            payload.type === 'request' ? '🩸' :
            payload.type === 'message' ? '✉' :
            payload.type === 'offer' ? '🤝' :
            payload.type === 'offer-status' ? '✓' : '🔔';

        const iconClass =
            payload.type === 'request' ? 'bc-bell-request' :
            payload.type === 'message' ? 'bc-bell-message' :
            payload.type === 'offer' ? 'bc-bell-offer' : '';

        const item = document.createElement('a');
        item.href = payload.url || '#';
        item.className = 'bc-bell-item is-new';
        item.innerHTML =
            '<span class="bc-bell-item-icon ' + iconClass + '">' + icon + '</span>' +
            '<span class="bc-bell-item-body">' +
            '  <span class="bc-bell-item-text">' + escapeHtml(payload.title || '') + '</span>' +
            '  <span class="bc-bell-item-sub">' + escapeHtml(payload.message || '') + '</span>' +
            '  <span class="bc-bell-item-time">Just now</span>' +
            '</span>';

        list.insertBefore(item, list.firstChild);

        setTimeout(() => item.classList.remove('is-new'), 3000);

        const items = list.querySelectorAll('.bc-bell-item');
        if (items.length > 8) {
            items[items.length - 1].remove();
        }
    }

    // ==================== SIGNALR ====================
    function connectSignalR() {
        if (typeof signalR === 'undefined') {
            console.warn('[Notif] SignalR client not loaded');
            return;
        }

        const connection = new signalR.HubConnectionBuilder()
            .withUrl(HUB_URL)
            .withAutomaticReconnect([0, 2000, 5000, 10000, 30000])
            .configureLogging(signalR.LogLevel.Warning)
            .build();

        connection.on('ReceiveNotification', function (payload) {
            console.log('[Notif] Received:', payload);
            incrementBellBadge();
            prependNotificationItem(payload);
            playNotificationSound();
            showNotificationToast(payload);
        });

        function start() {
            connection.start()
                .then(function () { console.log('✅ SignalR connected'); })
                .catch(function (err) {
                    console.warn('[Notif] Connect failed, retrying in 5s...', err);
                    setTimeout(start, 5000);
                });
        }

        connection.onreconnected(function () { console.log('✅ SignalR reconnected'); });
        connection.onclose(function () {
            console.warn('[Notif] Disconnected, retrying...');
            setTimeout(start, 5000);
        });

        start();

        // Unlock audio on first user interaction
        document.addEventListener('click', function unlock() {
            ensureAudioContext();
            document.removeEventListener('click', unlock);
        }, { once: true });
    }

    // ==================== INIT ====================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', connectSignalR);
    } else {
        connectSignalR();
    }
})();