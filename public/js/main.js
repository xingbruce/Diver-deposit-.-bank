
const show = (id) => document.getElementById(id)?.classList.remove('hidden');
const hide = (id) => document.getElementById(id)?.classList.add('hidden');

let tempUserId = null;

// STEP 1
document.getElementById('login-step-1')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    hide('error'); show('loading');

    const payload = {
        username: document.getElementById('username').value.trim(),
        password: document.getElementById('password').value.trim()
    };

    try {
        const res = await fetch('/api/login-step-1', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await res.json();
        hide('loading');

        if (result.error) {
            show('error'); setTimeout(() => hide('error'), 3000); return;
        }

        tempUserId = result.id;
        document.getElementById('step1-container').classList.add('hidden');
        document.getElementById('step2-container').classList.remove('hidden');
    } catch (err) {
        console.error('Step1 failed', err);
        hide('loading'); show('error'); setTimeout(() => hide('error'), 3000);
    }
});

// STEP 2
document.getElementById('login-step-2')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    hide('error'); show('loading');

    const payload = {
        user_id: tempUserId,
        security_code: document.getElementById('security-code').value.trim(),
        favorite_food: document.getElementById('favorite-food').value.trim()
    };

    try {
        const res = await fetch('/api/login-step-2', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await res.json();
        hide('loading');

        if (result.error) {
            show('error'); setTimeout(() => hide('error'), 3000); return;
        }

        const redirectUrl = result.role === 'admin' ? `/admin.html?admin_id=${result.id}` : `/dashboard.html?id=${result.id}`;
        window.location.href = redirectUrl;
    } catch (err) {
        console.error('Step2 failed', err);
        hide('loading'); show('error'); setTimeout(() => hide('error'), 3000);
    }
});

// Register and helpers (register-button, forgot-password) left as-is
document.getElementById('register-button')?.addEventListener('click', (e) => { e.preventDefault(); window.location.href = '/register.html'; });
document.getElementById('forgot-password')?.addEventListener('click', (e) => { e.preventDefault(); alert('Password reset coming soon.'); });

/* Admin creation and admin UI functions (loadUsers, create-user form handlers, etc.)
   — keep the admin-related handlers you already have in your main.js (from earlier),
   they call /api/admin/create-user and /api/admin/list-users which are implemented above.
*/

</html>
