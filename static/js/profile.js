const token = localStorage.getItem("token");

// Redirecionar para login se não houver token
if (!token) 
    {
    window.location.href = "/login";
    }


// Carregar dados do utilizador 
async function loadUser() 
    {
    try
        {
        const res = await fetch("/api/auth/user", 
            {
            headers: { "Authorization": `Bearer ${token}` }
            });

        // Token inválido ou expirado
        if (res.status === 401 || res.status === 422) 
            {
            localStorage.removeItem("token");
            window.location.href = "/login";
            return;
            }

            if (!res.ok) return;

        const user = await res.json();

        // Avatar com inical
        const initials = user.username.substring(0, 1).toUpperCase();
        document.getElementById("avatar").textContent = initials;

        // Formatar a data
        const date = new Date(user.created_at);
        const dataFormatada = date.toLocaleDateString("pt-PT", 
            {
            day: "2-digit",
            month: "long",
            year: "numeric"
            });

        // Lado esquerdo
        document.getElementById("profile-username").textContent = user.username;
        document.getElementById("profile-email").textContent    = user.email;
        document.getElementById("profile-badge").textContent    = `#${user.id}`;
        document.getElementById("profile-created").textContent  = dataFormatada;

        // Lado direito — detalhes
        document.getElementById("detail-username").textContent = user.username;
        document.getElementById("detail-email").textContent    = user.email;
        document.getElementById("detail-id").textContent       = user.id;
        document.getElementById("detail-created").textContent  = dataFormatada;

        } 
        catch (e) 
            {
            console.error("Erro ao carregar utilizador:", e);
            }
    }


/* ── Pedir reset de password via email ────────────────────── */
async function pedir_reset() {
    const email = document.getElementById("detail-email").textContent;
    const msgEl = document.getElementById("msg-reset");
    const btn   = document.getElementById("btn-reset");

    if (!email || email === "—") return;

    btn.disabled = true;

    try {
        const res  = await fetch("/api/auth/forgot_password", {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ email })
        });

        const data = await res.json();

        msgEl.textContent = data.message;
        msgEl.className   = res.ok ? "ok" : "err";
        msgEl.style.display = "block";

    } catch (e) {
        msgEl.textContent   = "Erro ao enviar pedido. Tenta novamente.";
        msgEl.className     = "err";
        msgEl.style.display = "block";
    } finally {
        // Reativar o botão após 5 segundos
        setTimeout(() => { btn.disabled = false; }, 5000);
    }
}


/* ── Navegação ────────────────────────────────────────────── */
function ver_dashboard() {
    window.location.href = "/dashboard";
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/login";
}


loadUser();