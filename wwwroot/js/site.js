// ============================================================
// BloodConnect — Site JavaScript
// ============================================================

(function () {
    'use strict';

    // --------------------------------------------------------
    // 1. Navbar scroll effect — shrink + shadow on scroll
    // --------------------------------------------------------
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        const onScroll = () => {
            if (window.scrollY > 20) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    // --------------------------------------------------------
    // 2. Auto-dismiss alerts after 5 seconds
    // --------------------------------------------------------
    document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(function () {
                if (alert.parentNode) {
                    alert.parentNode.removeChild(alert);
                }
            }, 500);
        }, 5000);
    });

    // --------------------------------------------------------
    // 3. Client-side phone number validation (fallback for browsers)
    // --------------------------------------------------------
    document.querySelectorAll('input[inputmode="numeric"]').forEach(function (input) {
        input.addEventListener('input', function () {
            // Sirf digits allow karo
            this.value = this.value.replace(/\D/g, '');
            // 10 digits se zyada mat hone do
            if (this.value.length > 10) {
                this.value = this.value.slice(0, 10);
            }
        });

        input.addEventListener('keypress', function (e) {
            // Sirf digits aur control keys allow karo
            const charCode = e.which ? e.which : e.keyCode;
            if (charCode > 31 && (charCode < 48 || charCode > 57)) {
                e.preventDefault();
            }
        });
    });

    // --------------------------------------------------------
    // 4. Confirm dialogs for dangerous actions
    // --------------------------------------------------------
    document.querySelectorAll('form[data-confirm]').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const message = form.getAttribute('data-confirm');
            if (message && !window.confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // --------------------------------------------------------
    // 5. Smooth scroll for anchor links
    // --------------------------------------------------------
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#' || targetId === '#!') return;

            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // --------------------------------------------------------
    // 6. Fade-in animation for cards on scroll (IntersectionObserver)
    // --------------------------------------------------------
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        document.querySelectorAll('.card, .trust-icon, .how-step-number')
            .forEach(function (el) {
                el.classList.add('fade-in-ready');
                observer.observe(el);
            });
    }

    // --------------------------------------------------------
    // 7. Prevent double-submit on forms (extra safety)
    // --------------------------------------------------------
    document.querySelectorAll('form').forEach(function (form) {
        form.addEventListener('submit', function () {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !form.dataset.noDisable) {
                setTimeout(function () {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Please wait…';
                }, 10);
            }
        });
    });

    // --------------------------------------------------------
    // 8. Bootstrap tooltips (if any elements use data-bs-toggle="tooltip")
    // --------------------------------------------------------
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
            new bootstrap.Tooltip(el);
        });
    }

})();
/* ============================================================
   HOMEPAGE V2 — Animated counters + scroll reveal
   ============================================================ */
(function () {
    'use strict';

    // Animated number counters
    function animateCounter(el) {
        const target = parseInt(el.getAttribute('data-count'), 10) || 0;
        if (target === 0) { el.textContent = '0'; return; }

        const duration = 1600;
        const start = performance.now();
        const startVal = 0;

        function tick(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            // easeOutExpo
            const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
            const current = Math.round(startVal + (target - startVal) * eased);
            el.textContent = current.toLocaleString();
            if (progress < 1) requestAnimationFrame(tick);
        }

        requestAnimationFrame(tick);
    }

    // IntersectionObserver for counters + reveal
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.4 });

    document.querySelectorAll('[data-count]').forEach(el => {
        counterObserver.observe(el);
    });

    // Scroll reveal
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal').forEach(el => {
        revealObserver.observe(el);
    });

})();