function submeter() {

    // Obter os valores dos campos
    const token = new URLSearchParams(window.location.search).get("token");
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("confirm_password").value;

    // Fazer o FETCH
    fetch(`/api/auth/reset_password/${token}`,
            {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ password, confirm_password })
            }
        )

    // Transformar a resposta em JSON (guardamos o status antes)
    .then(response => response.json().then(data => ({ ok: response.ok, data })))

    // Verificar se o pedido foi bem-sucedido
    .then(({ ok, data }) =>
            {
            if (ok)
                {
                window.location.href = "/login";
                }
            else
                {
                // Editamos o campo "erro" para mostrar a mensagem de erro retornada pela API
                document.getElementById("erro").textContent = data.message;
                }
            }
         )

    // Se ocorrer um erro na requisição, mostramos uma mensagem de erro
    .catch(error => {
        console.error("Erro ao resetar password:", error);
        document.getElementById("erro").textContent = "Ocorreu um erro. Por favor, tente novamente mais tarde.";
    });
}