/* ═══════════════════════════════════════════════════════════
   BloodConnect — Animation Orchestrator v3
   ═══════════════════════════════════════════════════════════ */
(function () {
    'use strict';

    /* ═══════════════════════════════════════════════════════
       §0 — SOUND SYSTEM (Web Audio API, no files)
       Louder + warmer: master gain + compressor + harmonic layering
       ═══════════════════════════════════════════════════════ */
    const Sound = (function () {
        let ctx = null;
        let master = null;
        let compressor = null;
        let muted = localStorage.getItem('bc-sound-muted') === 'true';

        function getCtx() {
            if (!ctx) {
                try {
                    ctx = new (window.AudioContext || window.webkitAudioContext)();

                    // Compressor — prevents clipping, glues sounds together
                    compressor = ctx.createDynamicsCompressor();
                    compressor.threshold.value = -14;
                    compressor.knee.value = 14;
                    compressor.ratio.value = 5;
                    compressor.attack.value = 0.003;
                    compressor.release.value = 0.25;

                    // Master gain
                    master = ctx.createGain();
                    master.gain.value = 1.0;

                    master.connect(compressor);
                    compressor.connect(ctx.destination);
                } catch (e) { return null; }
            }
            if (ctx.state === 'suspended') ctx.resume();
            return ctx;
        }

        /**
         * Play a tone.
         * @param {object} opts
         *   freq      — base frequency (Hz)
         *   type      — 'sine' | 'triangle' | 'square' | 'sawtooth'
         *   dur       — duration (seconds)
         *   vol       — peak volume (0..1) — 0.2 to 0.3 is punchy but safe
         *   sweep     — optional frequency target for exponential sweep
         *   delay     — start delay (seconds)
         *   detune    — cents detune
         *   harmonic  — add a richer 2nd layer for warmth
         */
        function tone({ freq, type = 'sine', dur = 0.15, vol = 0.25, sweep = null, delay = 0, detune = 0, harmonic = false }) {
            if (muted) return;
            const ac = getCtx();
            if (!ac) return;
            try {
                const start = ac.currentTime + delay;

                // ── Main oscillator ──
                const osc = ac.createOscillator();
                const gain = ac.createGain();
                osc.type = type;
                osc.frequency.setValueAtTime(freq, start);
                if (sweep) osc.frequency.exponentialRampToValueAtTime(sweep, start + dur);
                if (detune) osc.detune.value = detune;

                // Envelope (attack → decay → tail)
                gain.gain.setValueAtTime(0.0001, start);
                gain.gain.exponentialRampToValueAtTime(vol, start + 0.01);
                gain.gain.exponentialRampToValueAtTime(vol * 0.55, start + dur * 0.5);
                gain.gain.exponentialRampToValueAtTime(0.0001, start + dur);

                osc.connect(gain);
                gain.connect(master);
                osc.start(start);
                osc.stop(start + dur + 0.05);

                // ── Harmonic layer (adds warmth/presence) ──
                if (harmonic) {
                    const osc2 = ac.createOscillator();
                    const gain2 = ac.createGain();
                    osc2.type = 'triangle';
                    osc2.frequency.setValueAtTime(freq * 2, start);
                    osc2.detune.value = 5;

                    gain2.gain.setValueAtTime(0.0001, start);
                    gain2.gain.exponentialRampToValueAtTime(vol * 0.32, start + 0.012);
                    gain2.gain.exponentialRampToValueAtTime(0.0001, start + dur);

                    osc2.connect(gain2);
                    gain2.connect(master);
                    osc2.start(start);
                    osc2.stop(start + dur + 0.05);
                }
            } catch (e) { /* silent */ }
        }

        return {
            success() {
                tone({ freq: 523.25, dur: 0.14, vol: 0.28, harmonic: true });          // C5
                tone({ freq: 783.99, dur: 0.20, vol: 0.25, delay: 0.09, harmonic: true }); // G5
                tone({ freq: 1046.5, dur: 0.30, vol: 0.24, delay: 0.20, harmonic: true }); // C6
            },
            error() {
                tone({ freq: 220, type: 'sawtooth', dur: 0.18, vol: 0.22, sweep: 110 });
                tone({ freq: 180, type: 'sawtooth', dur: 0.24, vol: 0.20, sweep: 90, delay: 0.12 });
            },
            click() {
                tone({ freq: 1600, type: 'triangle', dur: 0.04, vol: 0.11 });
                tone({ freq: 2400, type: 'sine', dur: 0.03, vol: 0.06 });
            },
            notify() {
                tone({ freq: 880, dur: 0.12, vol: 0.26, harmonic: true });       // A5
                tone({ freq: 1318.5, dur: 0.20, vol: 0.23, delay: 0.08, harmonic: true }); // E6
            },
            whoosh() {
                tone({ freq: 500, type: 'sine', dur: 0.25, vol: 0.13, sweep: 90 });
            },
            chime() {
                tone({ freq: 659.25, dur: 0.18, vol: 0.27, harmonic: true });      // E5
                tone({ freq: 987.77, dur: 0.30, vol: 0.25, delay: 0.10, harmonic: true }); // B5
            },
            isMuted: () => muted,
            toggle() {
                muted = !muted;
                localStorage.setItem('bc-sound-muted', muted ? 'true' : 'false');
                if (!muted) Sound.click();
                return muted;
            },
            prime() {
                const ac = getCtx();
                if (ac && ac.state === 'suspended') ac.resume();
            }
        };
    })();

    window.bcSound = Sound;

    // Prime audio context on first user interaction (autoplay policy)
    ['click', 'touchstart', 'keydown'].forEach(evt => {
        window.addEventListener(evt, () => Sound.prime(), { once: true, passive: true });
    });

    /* ═══════════════════════════════════════════════════════
       §1 — TOAST SYSTEM
       ═══════════════════════════════════════════════════════ */
    const toastStack = document.getElementById('toast-stack');

    const ICONS = {
        success: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><polyline points="20 6 9 17 4 12"/></svg>',
        error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>',
        warning: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
    };

    function showToast(message, type = 'info', duration = 4500) {
        if (!toastStack || !message) return;

        if (type === 'success') Sound.success();
        else if (type === 'error') Sound.error();
        else if (type === 'warning') Sound.error();
        else Sound.notify();

        const el = document.createElement('div');
        el.className = `toast-item toast-${type}`;
        el.innerHTML = `
            <span class="toast-icon">${ICONS[type] || ICONS.info}</span>
            <div class="toast-content">${message}</div>
            <button type="button" class="toast-close" aria-label="Close">&times;</button>
        `;
        toastStack.appendChild(el);

        const close = () => {
            el.classList.add('is-leaving');
            setTimeout(() => el.remove(), 220);
        };
        el.querySelector('.toast-close').addEventListener('click', close);
        if (duration > 0) setTimeout(close, duration);
    }

    window.bcToast = showToast;

    /* ═══════════════════════════════════════════════════════
       §2 — AUTO-TOAST FROM TempData
       ═══════════════════════════════════════════════════════ */
    document.querySelectorAll('[data-toast]').forEach(el => {
        const type = el.getAttribute('data-toast') || 'info';
        const msg = el.getAttribute('data-toast-msg') || el.textContent.trim();
        if (msg) showToast(msg, type);
        el.remove();
    });

    /* ═══════════════════════════════════════════════════════
       §3 — CUSTOM CONFIRM MODAL
       ═══════════════════════════════════════════════════════ */
    const confirmEl = document.getElementById('bc-confirm-modal');
    let pendingAction = null;

    function openConfirm({ title, message, confirmText, confirmClass, icon, sound }) {
        if (!confirmEl) return;
        confirmEl.querySelector('.confirm-icon').className = 'confirm-icon ' + (icon || 'confirm-danger');
        confirmEl.querySelector('.confirm-title').textContent = title || 'Are you sure?';
        confirmEl.querySelector('.confirm-message').textContent = message || 'This action cannot be undone.';
        const confirmBtn = confirmEl.querySelector('[data-confirm-accept]');
        confirmBtn.textContent = confirmText || 'Confirm';
        confirmBtn.className = 'btn ' + (confirmClass || 'btn-danger');
        confirmEl.classList.add('is-active');
        confirmEl.setAttribute('aria-hidden', 'false');

        if (sound) sound();
        else Sound.notify();
    }

    function closeConfirm() {
        if (!confirmEl) return;
        confirmEl.classList.remove('is-active');
        confirmEl.setAttribute('aria-hidden', 'true');
        pendingAction = null;
    }

    if (confirmEl) {
        confirmEl.querySelector('[data-confirm-cancel]').addEventListener('click', () => {
            Sound.click();
            closeConfirm();
        });
        confirmEl.querySelector('[data-confirm-accept]').addEventListener('click', () => {
            Sound.success();
            const action = pendingAction;
            closeConfirm();
            if (typeof action === 'function') action();
        });
        confirmEl.addEventListener('click', (e) => {
            if (e.target === confirmEl) closeConfirm();
        });
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && confirmEl.classList.contains('is-active')) closeConfirm();
        });
    }

    /* ═══════════════════════════════════════════════════════
       §4 — AUTO-INTERCEPT NATIVE confirm()
       ═══════════════════════════════════════════════════════ */
    function extractConfirmMessage(str) {
        if (!str) return null;
        const m = str.match(/confirm\s*\(\s*(['"`])([\s\S]*?)\1\s*\)/);
        return m ? m[2] : null;
    }

    document.addEventListener('submit', (e) => {
        const form = e.target;
        if (form.dataset.confirmBypass === 'true') return;
        if (form.dataset.confirmHandled === 'true') return;

        const onsubmit = form.getAttribute('onsubmit') || '';
        const message = extractConfirmMessage(onsubmit);
        if (!message) return;

        e.preventDefault();
        e.stopImmediatePropagation();

        const msgLower = message.toLowerCase();
        let title = 'Are you sure?';
        let confirmText = 'Confirm';
        let confirmClass = 'btn-danger';
        let icon = 'confirm-danger';
        let sound = Sound.notify;

        if (msgLower.includes('delete')) {
            title = 'Delete this item?';
            confirmText = 'Delete';
            sound = () => Sound.error();
        } else if (msgLower.includes('accept')) {
            title = 'Accept this offer?';
            confirmText = 'Accept';
            confirmClass = 'btn-success';
            icon = 'confirm-info';
            sound = () => Sound.chime();
        } else if (msgLower.includes('reject') || msgLower.includes('cancel')) {
            title = 'Reject this offer?';
            confirmText = 'Reject';
            confirmClass = 'btn-outline-danger';
            icon = 'confirm-warning';
            sound = () => Sound.notify();
        } else if (msgLower.includes('fulfil') || msgLower.includes('complete')) {
            title = 'Mark as completed?';
            confirmText = 'Mark Complete';
            confirmClass = 'btn-success';
            icon = 'confirm-info';
            sound = () => Sound.chime();
        } else if (msgLower.includes('ban')) {
            title = msgLower.includes('unban') ? 'Unban this user?' : 'Ban this user?';
            confirmText = msgLower.includes('unban') ? 'Unban' : 'Ban';
            confirmClass = msgLower.includes('unban') ? 'btn-outline-warning' : 'btn-danger';
            icon = 'confirm-warning';
        } else if (msgLower.includes('promote') || msgLower.includes('make admin')) {
            title = 'Promote to Admin?';
            confirmText = 'Make Admin';
            confirmClass = 'btn-success';
            icon = 'confirm-info';
        } else if (msgLower.includes('remove admin') || msgLower.includes('demote')) {
            title = 'Remove Admin role?';
            confirmText = 'Remove Admin';
            confirmClass = 'btn-outline-warning';
            icon = 'confirm-warning';
        } else if (msgLower.includes('offer') || msgLower.includes('donate')) {
            title = 'Send donation offer?';
            confirmText = 'Send Offer';
            confirmClass = 'btn-danger';
            icon = 'confirm-info';
            sound = () => Sound.chime();
        }

        pendingAction = () => {
            form.dataset.confirmBypass = 'true';
            form.removeAttribute('onsubmit');
            form.submit();
        };
        openConfirm({ title, message, confirmText, confirmClass, icon, sound });
    }, true);

    /* ═══════════════════════════════════════════════════════
       §5 — BUTTON LOADING ON FORM SUBMIT
       ═══════════════════════════════════════════════════════ */
    document.addEventListener('submit', (e) => {
        const form = e.target;
        if (form.dataset.confirmBypass !== 'true') {
            const onsubmit = form.getAttribute('onsubmit') || '';
            if (extractConfirmMessage(onsubmit)) return;
            if (form.matches('form[data-confirm]') && form.dataset.confirmed !== 'true') return;
        }
        if (form.checkValidity && !form.checkValidity()) return;

        const btn = form.querySelector('button[type="submit"]:not([data-no-loading])');
        if (btn && !btn.classList.contains('is-loading')) {
            btn.classList.add('is-loading');
            setTimeout(() => btn.classList.remove('is-loading'), 20000);
        }
    });

    /* ═══════════════════════════════════════════════════════
       §6 — BUTTON RIPPLE + SOUND
       ═══════════════════════════════════════════════════════ */
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn, .btn-hero-primary, .btn-cta-primary, .btn-search, .chip');
        if (!btn) return;

        Sound.click();

        const rect = btn.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        const ripple = document.createElement('span');
        ripple.className = 'btn-ripple';
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        btn.appendChild(ripple);
        setTimeout(() => ripple.remove(), 620);
    });

    /* ═══════════════════════════════════════════════════════
       §7 — VALIDATION SHAKE
       ═══════════════════════════════════════════════════════ */
    document.addEventListener('invalid', (e) => {
        const field = e.target;
        if (!field.classList) return;
        field.classList.add('field-shake');
        Sound.error();
        setTimeout(() => field.classList.remove('field-shake'), 520);
    }, true);

    document.querySelectorAll('.input-validation-error').forEach(el => {
        el.classList.add('field-shake');
        setTimeout(() => el.classList.remove('field-shake'), 520);
    });

    /* ═══════════════════════════════════════════════════════
       §8 — REVEAL ON SCROLL
       ═══════════════════════════════════════════════════════ */
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal, .reveal-stagger').forEach(el => {
        revealObserver.observe(el);
    });

    /* ═══════════════════════════════════════════════════════
       §9 — MINIMAL TOP PROGRESS BAR (loader)
       Only shows if navigation takes > 280ms. Quick navs = no bar.
       ═══════════════════════════════════════════════════════ */
    const loader = document.getElementById('page-loader');
    let loaderTimer = null;

    function showLoader() {
        if (loader) loader.classList.add('is-active');
    }
    function hideLoader() {
        clearTimeout(loaderTimer);
        if (loader) loader.classList.remove('is-active');
    }

    window.bcShowLoader = () => showLoader();
    window.bcHideLoader = () => hideLoader();

    document.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (!link) return;
        if (link.target === '_blank') return;
        if (link.hasAttribute('data-no-loader')) return;
        if (link.dataset.confirmBypass === 'true') return;
        const href = link.getAttribute('href');
        if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) return;

        try {
            const url = new URL(link.href, window.location.origin);
            if (url.origin !== window.location.origin) return;
        } catch (err) { return; }

        clearTimeout(loaderTimer);
        loaderTimer = setTimeout(() => showLoader(), 280);

        Sound.whoosh();
    });

    window.addEventListener('pageshow', () => hideLoader());
    window.addEventListener('beforeunload', () => clearTimeout(loaderTimer));

    /* ═══════════════════════════════════════════════════════
       §10 — WELCOME SPLASH
       ═══════════════════════════════════════════════════════ */
    const splash = document.getElementById('welcome-splash');
    if (splash) {
        splash.classList.add('is-active');
        Sound.chime();
        setTimeout(() => {
            splash.classList.add('is-leaving');
            setTimeout(() => splash.remove(), 600);
        }, 1700);
    }

    /* ═══════════════════════════════════════════════════════
       §11 — CONFETTI
       ═══════════════════════════════════════════════════════ */
    window.bcConfetti = function (count = 40) {
        const colors = ['#DC2626', '#FCD34D', '#D4A24C', '#047857', '#7F1D1D', '#F87171'];
        for (let i = 0; i < count; i++) {
            const piece = document.createElement('div');
            piece.className = 'confetti-piece';
            piece.style.left = Math.random() * 100 + 'vw';
            piece.style.background = colors[Math.floor(Math.random() * colors.length)];
            piece.style.animationDelay = (Math.random() * 0.5) + 's';
            piece.style.animationDuration = (2.2 + Math.random() * 1.5) + 's';
            piece.style.transform = `rotate(${Math.random() * 360}deg)`;
            document.body.appendChild(piece);
            setTimeout(() => piece.remove(), 4000);
        }
    };

    /* ═══════════════════════════════════════════════════════
       §12 — BLOOD DROP RAIN (on fulfill)
       ═══════════════════════════════════════════════════════ */
    window.bcBloodRain = function (count = 30) {
        for (let i = 0; i < count; i++) {
            const drop = document.createElement('div');
            drop.className = 'blood-drip';
            drop.style.left = Math.random() * 100 + 'vw';
            drop.style.animationDelay = (Math.random() * 0.6) + 's';
            drop.style.animationDuration = (2 + Math.random() * 1.5) + 's';
            drop.style.opacity = 0.5 + Math.random() * 0.5;
            document.body.appendChild(drop);
            setTimeout(() => drop.remove(), 4500);
        }
    };

    /* ═══════════════════════════════════════════════════════
       §13 — SPARKLE BURST (on success)
       ═══════════════════════════════════════════════════════ */
    window.bcSparkle = function (x, y) {
        const count = 12;
        for (let i = 0; i < count; i++) {
            const angle = (Math.PI * 2 * i) / count + Math.random() * 0.3;
            const distance = 40 + Math.random() * 60;
            const spark = document.createElement('div');
            spark.className = 'sparkle-particle';
            spark.style.left = x + 'px';
            spark.style.top = y + 'px';
            spark.style.setProperty('--dx', Math.cos(angle) * distance + 'px');
            spark.style.setProperty('--dy', Math.sin(angle) * distance + 'px');
            spark.style.background = Math.random() > 0.5 ? '#D4A24C' : '#FCD34D';
            document.body.appendChild(spark);
            setTimeout(() => spark.remove(), 900);
        }
    };

    // Auto-confetti + blood rain on fulfillment success
    const successNode = document.querySelector('[data-toast="success"]');
    if (successNode) {
        const msg = successNode.getAttribute('data-toast-msg') || '';
        if (/fulfil/i.test(msg)) {
            setTimeout(() => {
                window.bcConfetti(70);
                window.bcBloodRain(25);
                const flash = document.createElement('div');
                flash.className = 'success-flash';
                document.body.appendChild(flash);
                setTimeout(() => flash.remove(), 600);
            }, 500);
        } else if (/offer|accept|complete/i.test(msg)) {
            setTimeout(() => window.bcConfetti(40), 300);
        }
    }

    /* ═══════════════════════════════════════════════════════
       §14 — 3D CARD TILT
       ═══════════════════════════════════════════════════════ */
    const tiltSelectors = '.compat-card, .how-card, .stat-v2, .why-stat-card, .urgent-card';
    document.querySelectorAll(tiltSelectors).forEach(card => {
        card.classList.add('tilt-target');
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const cx = rect.width / 2;
            const cy = rect.height / 2;
            const rx = ((y - cy) / cy) * -5;
            const ry = ((x - cx) / cx) * 5;
            card.classList.add('is-tilting');
            card.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateZ(4px)`;
        });
        card.addEventListener('mouseleave', () => {
            card.classList.remove('is-tilting');
            card.style.transform = '';
        });
    });

    /* ═══════════════════════════════════════════════════════
       §15 — MAGNETIC BUTTONS
       ═══════════════════════════════════════════════════════ */
    const magneticSelectors = '.btn-hero-primary, .btn-cta-primary, .btn-search, .navbar-brand';
    document.querySelectorAll(magneticSelectors).forEach(btn => {
        btn.classList.add('btn-magnetic');
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            btn.classList.remove('is-snapping');
            btn.style.transform = `translate(${x * 0.18}px, ${y * 0.18}px)`;
        });
        btn.addEventListener('mouseleave', () => {
            btn.classList.add('is-snapping');
            btn.style.transform = '';
            setTimeout(() => btn.classList.remove('is-snapping'), 400);
        });
    });

    /* ═══════════════════════════════════════════════════════
       §16 — HERO CURSOR GLOW
       ═══════════════════════════════════════════════════════ */
    const hero = document.querySelector('.hero-v2');
    if (hero) {
        hero.addEventListener('mousemove', (e) => {
            const rect = hero.getBoundingClientRect();
            hero.style.setProperty('--mouse-x', (e.clientX - rect.left) + 'px');
            hero.style.setProperty('--mouse-y', (e.clientY - rect.top) + 'px');
        });
    }

    /* ═══════════════════════════════════════════════════════
       §17 — SOUND TOGGLE BUTTON (auto-inject into navbar)
       ═══════════════════════════════════════════════════════ */
    const navContainer = document.querySelector('header .navbar .container');
    if (navContainer) {
        const toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.className = 'sound-toggle' + (Sound.isMuted() ? ' is-muted' : '');
        toggle.setAttribute('aria-label', 'Toggle sound');
        toggle.title = 'Toggle sound';
        toggle.innerHTML = `
            <svg class="icon-on" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>
            <svg class="icon-off" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/></svg>
        `;
        toggle.addEventListener('click', () => {
            const isMuted = Sound.toggle();
            toggle.classList.toggle('is-muted', isMuted);
        });

        const btnGroup = navContainer.querySelector('.d-flex.gap-2');
        if (btnGroup) {
            btnGroup.insertBefore(toggle, btnGroup.firstChild);
        } else {
            navContainer.appendChild(toggle);
        }
    }

})();