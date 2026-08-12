const API_URL = "http://127.0.0.1:8000";
let currentTab = "login";

// --- INICIALIZAÇÃO ---
document.addEventListener("DOMContentLoaded", () => {
  // Preenche a data padrão do formulário como HOJE
  document.getElementById("tx-date").value = new Date().toISOString().split("T")[0];
  checkAuth();
});

function checkAuth() {
  const token = localStorage.getItem("token");
  const userEmail = localStorage.getItem("userEmail");

  if (token) {
    document.getElementById("auth-screen").classList.add("hidden");
    document.getElementById("app-screen").classList.remove("hidden");
    document.getElementById("user-email-display").innerText = userEmail || "Usuário Logado";
    loadDashboardData();
  } else {
    document.getElementById("auth-screen").classList.remove("hidden");
    document.getElementById("app-screen").classList.add("hidden");
  }
}

// --- CONTROLE DAS TABS DE AUTENTICAÇÃO ---
function switchAuthTab(tab) {
  currentTab = tab;
  document.getElementById("auth-error").innerText = "";
  
  if (tab === "login") {
    document.getElementById("tab-login").classList.add("active");
    document.getElementById("tab-register").classList.remove("active");
    document.getElementById("auth-submit-btn").innerText = "Acessar Conta";
  } else {
    document.getElementById("tab-register").classList.add("active");
    document.getElementById("tab-login").classList.remove("active");
    document.getElementById("auth-submit-btn").innerText = "Criar Minha Conta";
  }
}

// --- AUTENTICAÇÃO (LOGIN / REGISTRO) ---
async function handleAuth(event) {
  event.preventDefault();
  const email = document.getElementById("auth-email").value;
  const password = document.getElementById("auth-password").value;
  const errorEl = document.getElementById("auth-error");
  errorEl.innerText = "";

  try {
    if (currentTab === "register") {
      // 1. Cadastrar
      const res = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Erro ao cadastrar");
      
      alert("Conta criada com sucesso! Faça login.");
      switchAuthTab("login");
    } else {
      // 2. Login (Form Data exigido pelo OAuth2PasswordRequestForm)
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Falha no login");

      localStorage.setItem("token", data.access_token);
      localStorage.setItem("userEmail", email);
      checkAuth();
    }
  } catch (err) {
    errorEl.innerText = err.message;
  }
}

function logout() {
  localStorage.clear();
  checkAuth();
}

// --- CARREGAMENTO DO DASHBOARD ---
async function loadDashboardData() {
  const token = localStorage.getItem("token");
  const headers = { "Authorization": `Bearer ${token}` };

  try {
    // Busca Resumo (Cards)
    const resSummary = await fetch(`${API_URL}/transactions/summary`, { headers });
    const summary = await resSummary.json();
    
    document.getElementById("total-income").innerText = formatCurrency(summary.total_income);
    document.getElementById("total-expense").innerText = formatCurrency(summary.total_expense);
    document.getElementById("total-balance").innerText = formatCurrency(summary.balance);

    // Busca Histórico de Transações
    const resTx = await fetch(`${API_URL}/transactions`, { headers });
    const transactions = await resTx.json();
    
    renderTransactionsTable(transactions);
  } catch (err) {
    console.error("Erro ao carregar dados:", err);
  }
}

function renderTransactionsTable(transactions) {
  const tbody = document.getElementById("transactions-list");
  tbody.innerHTML = "";

  transactions.forEach(tx => {
    const tr = document.createElement("tr");
    const isReceita = tx.type === "receita";

    tr.innerHTML = `
      <td>${tx.description}</td>
      <td>${tx.category}</td>
      <td>${tx.date}</td>
      <td class="${isReceita ? 'val-receita' : 'val-despesa'}">
        ${isReceita ? '+' : '-'} ${formatCurrency(tx.value)}
      </td>
      <td>
        <button onclick="handleDeleteTransaction(${tx.id})" class="btn-delete" title="Excluir">🗑️</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// --- CRIAÇÃO DE TRANSAÇÃO ---
async function handleCreateTransaction(event) {
  event.preventDefault();
  const token = localStorage.getItem("token");

  const payload = {
    description: document.getElementById("tx-description").value,
    value: parseFloat(document.getElementById("tx-value").value),
    type: document.getElementById("tx-type").value,
    category: document.getElementById("tx-category").value,
    date: document.getElementById("tx-date").value
  };

  try {
    const res = await fetch(`${API_URL}/transactions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error("Erro ao salvar transação");

    // Limpa formulário e recarrega
    document.getElementById("tx-description").value = "";
    document.getElementById("tx-value").value = "";
    document.getElementById("tx-category").value = "";
    loadDashboardData();
  } catch (err) {
    alert(err.message);
  }
}

// --- EXCLUSÃO DE TRANSAÇÃO ---
async function handleDeleteTransaction(id) {
  if (!confirm("Deseja realmente apagar esta transação?")) return;
  const token = localStorage.getItem("token");

  try {
    const res = await fetch(`${API_URL}/transactions/${id}`, {
      method: "DELETE",
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (!res.ok) throw new Error("Erro ao deletar transação");
    loadDashboardData();
  } catch (err) {
    alert(err.message);
  }
}

function formatCurrency(val) {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);
}