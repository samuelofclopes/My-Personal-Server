function enviar_recuperacao() {

    // Obter os valores dos campos
    const email = document.getElementById("email").value;

    // Fazer o FETCH
    fetch("/api/auth/forgot_password",
            {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ email })
            }
        )

    // Transformar a resposta em JSON (guardamos o status antes)
    .then(response => response.json().then(data => ({ ok: response.ok, data })))

    // Verificar se o pedido foi bem-sucedido
    .then(({ ok, data }) =>
            {
            if (ok)
                {
                document.getElementById("sucesso").textContent = data.message;
                document.getElementById("erro").textContent = "";
                }
            else
                {
                document.getElementById("erro").textContent = data.message;
                }
            }
         )

    // Se ocorrer um erro na requisição, mostramos uma mensagem de erro
    .catch(error => {
        console.error("Erro ao enviar email de recuperação:", error);
        document.getElementById("erro").textContent = "Ocorreu um erro. Por favor, tente novamente mais tarde.";
    });
}