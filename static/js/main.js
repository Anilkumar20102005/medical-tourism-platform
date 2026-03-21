/* ================================================================
   HealinBelieve — Main JavaScript
   Nav · Stats · Forms · Filters · Flash auto-dismiss
   ================================================================ */

document.addEventListener('DOMContentLoaded', () => {

    // ─── Mobile Nav Toggle ────────────────────────────────────
    const toggle = document.getElementById('navToggle');
    const links  = document.getElementById('navLinks');
    if (toggle && links) {
        toggle.addEventListener('click', () => links.classList.toggle('open'));
        links.querySelectorAll('a').forEach(a =>
            a.addEventListener('click', () => links.classList.remove('open'))
        );
    }

    // ─── Navbar Scroll Effect ─────────────────────────────────
    const navbar = document.getElementById('mainNav');
    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.style.background = window.scrollY > 80
                ? 'rgba(10,15,26,.95)' : 'rgba(10,15,26,.8)';
        });
    }

    // ─── Stat Counter Animation ───────────────────────────────
    const counters = document.querySelectorAll('.stat-number[data-target]');
    if (counters.length) {
        const animateCounter = (el) => {
            const target = +el.dataset.target;
            const suffix = el.dataset.suffix || '';
            const dur = 2000;
            const start = performance.now();
            const step = (now) => {
                const p = Math.min((now - start) / dur, 1);
                const ease = 1 - (1 - p) * (1 - p);
                el.textContent = Math.floor(ease * target) + suffix;
                if (p < 1) requestAnimationFrame(step);
                else el.textContent = target + suffix;
            };
            requestAnimationFrame(step);
        };
        const observer = new IntersectionObserver(entries => {
            entries.forEach(e => {
                if (e.isIntersecting) { animateCounter(e.target); observer.unobserve(e.target); }
            });
        }, { threshold: 0.5 });
        counters.forEach(c => observer.observe(c));
    }

    // ─── Doctor Finder Form ───────────────────────────────────
    const form = document.getElementById('matchForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btnText   = form.querySelector('.btn-text');
            const btnLoader = form.querySelector('.btn-loader');
            const submitBtn = form.querySelector('#submitMatch');

            if (btnText) btnText.hidden = true;
            if (btnLoader) btnLoader.hidden = false;
            if (submitBtn) submitBtn.disabled = true;

            const payload = {
                specialty:      form.specialty.value,
                budget:         parseFloat(form.budget.value) || 0,
                country:        form.country.value,
                min_experience: parseInt(form.min_experience.value, 10) || 0,
            };

            try {
                const res = await fetch('/api/match', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });
                if (!res.ok) throw new Error('Server error');
                const data = await res.json();
                sessionStorage.setItem('matchResults', JSON.stringify(data));
                window.location.href = '/results';
            } catch (err) {
                alert('Something went wrong. Please try again.');
                console.error(err);
            } finally {
                if (btnText) btnText.hidden = false;
                if (btnLoader) btnLoader.hidden = true;
                if (submitBtn) submitBtn.disabled = false;
            }
        });
    }

    // ─── Directory Specialty Filters ──────────────────────────
    const filterBtns = document.querySelectorAll('.filter-btn[data-filter]');
    const doctorCards = document.querySelectorAll('.doctor-card[data-specialty]');
    if (filterBtns.length && doctorCards.length) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const filter = btn.dataset.filter;
                doctorCards.forEach(card => {
                    card.classList.toggle('hidden', filter !== 'all' && card.dataset.specialty !== filter);
                });
            });
        });
    }

    // ─── Flash Auto-Dismiss ───────────────────────────────────
    document.querySelectorAll('.flash').forEach(f => {
        setTimeout(() => { f.style.opacity = '0'; f.style.transform = 'translateX(20px)'; setTimeout(() => f.remove(), 300); }, 5000);
    });

    // ─── Message form receiver_id sync ────────────────────────
    const msgForm = document.querySelector('.msg-form');
    if (msgForm) {
        const select = msgForm.querySelector('select[name=hospital_id]');
        const hidden = msgForm.querySelector('input[name=receiver_id]');
        if (select && hidden) {
            select.addEventListener('change', () => { hidden.value = select.value; });
        }
    }

});
