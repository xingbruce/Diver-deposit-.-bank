import { createClient } from '@supabase/supabase-js';
import i18next from 'i18next';

const supabaseUrl = process.env.SUPABASE_URL || 'https://dodijnhzghlpgmdddklr.supabase.co';
const supabaseKey = process.env.SUPABASE_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRvZGlqbmh6Z2hscGdtZGRka2xyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM0NTE3MTksImV4cCI6MjA2OTAyNzcxOX0.soz1ofVIZ3NeWkcE1yUCIylFiVry5nwvc9PvHn7TZQQ';
const supabase = createClient(supabaseUrl, supabaseKey);

i18next.init({
    lng: 'en',
    resources: {
        en: { translation: { 
            welcome: 'Welcome to Diver Deposit Bank',
            since: 'Since 1988',
            login: 'Login',
            username: 'Username',
            password: 'Password',
            security_code: "What's your security code?",
            favorite_food: "What's your favorite food?",
            invalid: 'Invalid credentials',
            balance: 'Balance',
            account_number: 'Account Number',
            deposit: 'Deposit',
            withdraw: 'Withdraw',
            transfer: 'Transfer',
            statement: 'Download Statement',
            loan: 'Apply for a Loan',
            apply: 'Apply',
            history: 'Transaction History',
            broker: 'Broker',
            crypto: 'Crypto Trading',
            support: 'Customer Support',
            support_placeholder: 'Leave your complaint...',
            create: 'Create User',
            assign: 'Assign Broker'
        } },
        es: { translation: { 
            welcome: 'Bienvenido a Diver Deposit Bank',
            since: 'Desde 1988',
            login: 'Iniciar sesión',
            username: 'Nombre de usuario',
            password: 'Contraseña',
            security_code: '¿Cuál es tu código de seguridad?',
            favorite_food: '¿Cuál es tu comida favorita?',
            invalid: 'Credenciales inválidas',
            balance: 'Saldo',
            account_number: 'Número de cuenta',
            deposit: 'Depósito',
            withdraw: 'Retiro',
            transfer: 'Transferencia',
            statement: 'Descargar estado de cuenta',
            loan: 'Solicitar un préstamo',
            apply: 'Solicitar',
            history: 'Historial de transacciones',
            broker: 'Corredor',
            crypto: 'Comercio de criptomonedas',
            support: 'Soporte al cliente',
            support_placeholder: 'Deja tu queja...',
            create: 'Crear usuario',
            assign: 'Asignar corredor'
        } },
        ko: { translation: { 
            welcome: 'Diver Deposit Bank에 오신 것을 환영합니다',
            since: '1988년부터',
            login: '로그인',
            username: '사용자 이름',
            password: '비밀번호',
            security_code: '보안 코드는 무엇입니까?',
            favorite_food: '좋아하는 음식은 무엇입니까?',
            invalid: '잘못된 자격 증명',
            balance: '잔액',
            account_number: '계좌 번호',
            deposit: '입금',
            withdraw: '출금',
            transfer: '이체',
            statement: '명세서 다운로드',
            loan: '대출 신청',
            apply: '신청',
            history: '거래 내역',
            broker: '브로커',
            crypto: '암호화폐 거래',
            support: '고객 지원',
            support_placeholder: '불만 사항을 남겨주세요...',
            create: '사용자 생성',
            assign: '브로커 지정'
        } },
        zh: { translation: { 
            welcome: '欢迎体验Diver Deposit Bank',
            since: '自1988年以来',
            login: '登录',
            username: '用户名',
            password: '密码',
            security_code: '您的安全代码是什么？',
            favorite_food: '您最喜欢的食物是什么？',
            invalid: '无效凭据',
            balance: '余额',
            account_number: '账户号码',
            deposit: '存款',
            withdraw: '取款',
            transfer: '转账',
            statement: '下载对账单',
            loan: '申请贷款',
            apply: '申请',
            history: '交易历史',
            broker: '经纪人',
            crypto: '加密货币交易',
            support: '客户支持',
            support_placeholder: '留下您的投诉...',
            create: '创建用户',
            assign: '分配经纪人'
        } }
    }
}).then(() => {
    document.getElementById('language-select')?.addEventListener('change', (e) => {
        i18next.changeLanguage(e.target.value);
        updateUI();
    });
    updateUI();
});

function updateUI() {
    document.querySelectorAll('[data-i18n]').forEach(elem => elem.textContent = i18next.t(elem.dataset.i18n));
    document.querySelectorAll('input[data-i18n-placeholder]').forEach(elem => elem.placeholder = i18next.t(elem.dataset.i18nPlaceholder));
}

document.getElementById('login-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        security_code: document.getElementById('security-code').value,
        favorite_food: document.getElementById('favorite-food').value
    };
    document.getElementById('loading').classList.remove('hidden');
    const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    document.getElementById('loading').classList.add('hidden');
    const result = await response.json();
    if (result.error) {
        document.getElementById('error').classList.remove('hidden');
        setTimeout(() => document.getElementById('error').classList.add('hidden'), 3000);
    } else {
        document.getElementById('success').classList.remove('hidden');
        setTimeout(() => {
            document.getElementById('success').classList.add('hidden');
            const redirectUrl = result.role === 'admin' ? `/admin.html?admin_id=${result.id}` : `/dashboard.html?id=${result.id}`;
            window.location.href = redirectUrl;
            if (redirectUrl.includes('dashboard.html')) {
                const urlParams = new URLSearchParams(window.location.search);
                const userId = urlParams.get('id');
                if (userId) loadDashboard(userId);
            }
        }, 1000);
    }
});

async function loadDashboard(userId) {
    try {
        const { data, error } = await supabase.from('users').select('*').eq('id', userId).single();
        if (error) throw error;
        document.getElementById('balance').textContent = data.balance.toFixed(2);
        document.getElementById('account-number').textContent = data.account_number;
        document.getElementById('card-last4').textContent = `Card Last 4: ${data.account_number.slice(-4)}`;
        document.getElementById('investment-funds').textContent = `Investment Funds: ${data.investment_funds.toFixed(2)}`;
        const { data: broker } = await supabase.from('brokers').select('*').eq('user_id', userId).maybeSingle();
        if (broker) {
            document.getElementById('broker-name').textContent = broker.name;
            document.getElementById('broker-balance').textContent = `$${broker.balance.toFixed(2)}`;
        }
        const { data: transactions } = await supabase.from('transactions').select('*').eq('user_id', userId);
        document.getElementById('transaction-list').innerHTML = transactions.map((tx, index) => `<li class="animate-slide-in" style="animation-delay: ${index * 0.1}s">${tx.date}: ${tx.type} - ${tx.amount.toFixed(2)} - ${tx.description}</li>`).join('');

        const { data: loanCompanies } = await supabase.from('loan_companies').select('*');
        document.getElementById('loan-company').innerHTML = loanCompanies.map(company => `<option value="${company.id}">${company.name} (${company.interest_rate}%)</option>`).join('');

        const { data: bitcoinExchanges } = await supabase.from('bitcoin_exchanges').select('*');
        document.getElementById('bitcoin-table').innerHTML = `
            <div class="grid grid-cols-3 gap-2">
                ${bitcoinExchanges.map(exchange => `<div class="bg-blue-100 p-2 rounded">${exchange.name}: ${exchange.price_per_btc.toFixed(2)}</div>`).join('')}
            </div>`;

        const { data: stockExchanges } = await supabase.from('stock_exchanges').select('*');
        document.getElementById('stock-table').innerHTML = `
            <div class="grid grid-cols-3 gap-2">
                ${stockExchanges.map(stock => `<div class="bg-blue-100 p-2 rounded">${stock.stock_symbol}: ${stock.price.toFixed(2)}</div>`).join('')}
            </div>`;
    } catch (error) {
        console.error('Error loading dashboard:', error.message);
        alert('Failed to load dashboard. Please try again.');
    }
}

async function simulateAction(type) {
    const userId = new URLSearchParams(window.location.search).get('id');
    const response = await fetch('/api/transactions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, type, amount: 100, description: `${type} test` })
    });
    const result = await response.json();
    showNotification(`${type.charAt(0).toUpperCase() + type.slice(1)} completed`);
    if (userId) await loadDashboard(userId);
}

async function simulateLoan() {
    const userId = new URLSearchParams(window.location.search).get('id');
    const loanCompanyId = document.getElementById('loan-company').value;
    const { data: company } = await supabase.from('loan_companies').select('max_loan_amount').eq('id', loanCompanyId).single();
    const loanAmount = company.max_loan_amount * Math.random();
    const response = await supabase.table('transactions').insert({
        user_id: userId,
        type: 'loan',
        amount: loanAmount,
        description: `Loan from ${company.name}`
    }).execute();
    showNotification('Loan application submitted');
    if (userId) await loadDashboard(userId);
}

function downloadStatement() {
    const doc = new jsPDF();
    doc.text('Diver Deposit Bank Statement', 10, 10);
    doc.text(`Account Number: ${document.getElementById('account-number').textContent}`, 10, 20);
    doc.text(`Balance: ${document.getElementById('balance').textContent}`, 10, 30);
    doc.text('Transactions:', 10, 40);
    const transactions = document.getElementById('transaction-list').innerHTML.split('<li>').slice(1);
    transactions.forEach((tx, i) => doc.text(tx.replace('</li>', ''), 10, 50 + i * 10));
    doc.save('statement.pdf');
}

function sendChatMessage() {
    const messageInput = document.getElementById('support-message');
    if (!messageInput.value) return;
    const chatMessages = document.getElementById('chat-messages');
    const timestamp = new Date().toLocaleTimeString();
    chatMessages.innerHTML += `<div class="bg-blue-100 p-2 rounded mb-2">${messageInput.value} <span class="text-xs text-gray-500">${timestamp}</span></div>`;
    messageInput.value = '';
    setTimeout(() => {
        chatMessages.innerHTML += `<div class="bg-gray-100 p-2 rounded mb-2">Thank you! Our 24/7 team will respond shortly. <span class="text-xs text-gray-500">${timestamp}</span></div>`;
        chatMessages.scrollTop = chatMessages.scrollHeight;
        showNotification('New support message');
    }, 1000);
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-green-500 text-white p-2 rounded shadow-lg animate-fade-in';
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}

document.getElementById('dark-mode-toggle')?.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
});

document.getElementById('create-user-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        admin_id: new URLSearchParams(window.location.search).get('admin_id'),
        username: document.getElementById('new-username').value,
        password: document.getElementById('new-password').value,
        security_code: document.getElementById('new-security-code').value,
        favorite_food: document.getElementById('new-favorite-food').value,
        balance: parseFloat(document.getElementById('new-balance').value),
        investment_funds: parseFloat(document.getElementById('new-investment-funds').value)
    };
    const response = await fetch('/api/admin/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    alert(result.message);
    loadUsers();
});

async function loadUsers() {
    const adminId = new URLSearchParams(window.location.search).get('admin_id');
    const response = await fetch(`/api/admin/users?admin_id=${adminId}`);
    const users = await response.json();
    document.getElementById('user-list').innerHTML = users.map(user => `
        <li class="bg-gray-100 p-2 rounded mb-2 flex justify-between">
            ${user.username} - ${user.account_number} - ${user.balance.toFixed(2)} - Funds: ${user.investment_funds.toFixed(2)}
            <button onclick="updateUser('${user.id}')" class="bg-blue-500 text-white p-1 rounded hover:bg-blue-600">Edit</button>
        </li>`).join('');
}

async function updateUser(userId) {
    const balance = prompt('Enter new balance:') || 0;
    const investmentFunds = prompt('Enter new investment funds:') || 0;
    const status = prompt('Enter status (active/frozen):') || 'active';
    const password = prompt('Enter new password (leave blank to skip):');
    const securityCode = prompt('Enter new security code (leave blank to skip):');
    const favoriteFood = prompt('Enter new favorite food (leave blank to skip):');
    const updates = { balance, status, investment_funds: investmentFunds };
    if (password) updates.password = bcrypt.hash(password);
    if (securityCode) updates.security_code = securityCode;
    if (favoriteFood) updates.favorite_food = favoriteFood;
    const response = await fetch(`/api/admin/users/${userId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates)
    });
    const result = await response.json();
    alert(result.message);
    loadUsers();
}

if (window.location.pathname.includes('dashboard.html')) {
    const userId = new URLSearchParams(window.location.search).get('id');
    if (userId) loadDashboard(userId);
} else if (window.location.pathname.includes('admin.html')) {
    loadUsers();
}
