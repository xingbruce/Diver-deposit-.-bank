<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diver Deposit Bank</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/css/styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2" defer></script>
    <script src="/js/main.js" defer></script>
</head>
<body class="bg-gray-100 min-h-screen">
    <header class="bg-blue-900 text-white p-4 flex justify-between items-center">
        <div class="text-xl font-bold" data-i18n="welcome">Diver Deposit Bank</div>
        <div class="flex space-x-4">
            <button id="dark-mode-toggle" class="p-2 rounded bg-gray-700 hover:bg-gray-600" data-i18n="dark_mode_toggle">Toggle Dark Mode</button>
            <select id="language-select" class="p-2 rounded bg-gray-700 text-white" data-i18n-select>
                <option value="en">English</option>
                <option value="es">Español</option>
                <option value="ko">한국어</option>
                <option value="zh">中文</option>
            </select>
        </div>
    </header>
    <main class="max-w-4xl mx-auto p-4 space-y-6">
        <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-semibold mb-4" data-i18n="account_overview">Account Overview</h2>
            <div id="balance" class="text-2xl font-bold mb-2"></div>
            <div id="account-number" class="text-sm text-gray-600 mb-2"></div>
            <div id="card-last4" class="bg-blue-100 p-4 rounded-lg mb-4">Card Last 4: ****</div>
            <div class="grid grid-cols-2 gap-4">
                <button onclick="simulateAction('deposit')" class="bg-green-500 text-white p-2 rounded hover:bg-green-600" data-i18n="deposit">Deposit</button>
                <button onclick="simulateAction('withdraw')" class="bg-red-500 text-white p-2 rounded hover:bg-red-600" data-i18n="withdraw">Withdraw</button>
                <button onclick="simulateAction('transfer')" class="bg-purple-500 text-white p-2 rounded hover:bg-purple-600" data-i18n="transfer">Transfer</button>
                <button onclick="downloadStatement()" class="bg-blue-500 text-white p-2 rounded hover:bg-blue-600" data-i18n="statement">Download Statement</button>
            </div>
            <form id="update-password-form" class="mt-4 space-y-2">
                <input type="password" id="new-password" placeholder="New Password" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" data-i18n-placeholder="new_password">
                <button type="submit" class="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 transition duration-200" data-i18n="update_password">Update Password</button>
            </form>
        </div>
        <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-semibold mb-4" data-i18n="loan">Loan Options</h2>
            <select id="loan-company" class="w-full p-2 border rounded mb-2"></select>
            <button onclick="simulateLoan()" class="bg-yellow-500 text-white p-2 rounded hover:bg-yellow-600" data-i18n="apply">Apply for Loan</button>
        </div>
        <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-semibold mb-4" data-i18n="history">Transaction History</h2>
            <ul id="transaction-list" class="space-y-2"></ul>
        </div>
        <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-semibold mb-4" data-i18n="broker">Investment Overview</h2>
            <div id="investment-funds" class="text-lg font-medium mb-2"></div>
            <div class="grid grid-cols-2 gap-4">
                <div id="bitcoin-table" class="overflow-x-auto"></div>
                <div id="stock-table" class="overflow-x-auto"></div>
            </div>
        </div>
        <div class="bg-white rounded-lg shadow-lg p-6">
            <h2 class="text-xl font-semibold mb-4" data-i18n="support">Customer Support</h2>
            <input type="text" id="support-message" placeholder="Leave your complaint..." class="w-full p-2 border rounded mb-2" data-i18n-placeholder="support_placeholder">
            <button onclick="sendChatMessage()" class="bg-blue-500 text-white p-2 rounded hover:bg-blue-600" data-i18n="support">Send</button>
            <div id="chat-messages" class="mt-2 h-40 overflow-y-auto border rounded p-2"></div>
        </div>
        <div class="bg-white rounded-lg shadow-lg p-6">
            <div class="dropdown">
                <button id="dashboard-menu" class="dropbtn bg-blue-500 text-white p-2 rounded hover:bg-blue-600" data-i18n="menu">Menu</button>
                <div id="dropdown-content" class="dropdown-content">
                    <a href="#" onclick="loadTransactions()" class="block px-4 py-2 text-gray-800 hover:bg-gray-200" data-i18n="history">Transactions</a>
                    <a href="#" onclick="loadInvestments()" class="block px-4 py-2 text-gray-800 hover:bg-gray-200" data-i18n="broker">Investments</a>
                    <a href="#" onclick="loadLoans()" class="block px-4 py-2 text-gray-800 hover:bg-gray-200" data-i18n="loan">Loans</a>
                </div>
            </div>
        </div>
    </main>
</body>
</html>
