function fazer_login() {

    // Obter os valores dos campos de username e senha
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    



    
    // Fazer o FECTH
    fetch("/api/auth/signin",
            {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ username, password })
            }
        )

    // Transformar a resposta em JSON
    .then(response => response.json())


    // Verificar se o login foi bem-sucedido
    .then(data =>
            {
            if (data.token) // Se o token existir, o login foi bem-sucedido, e guardamos o token e redirecionamos para o dashboard
                {
                localStorage.setItem("token", data.token);
                window.location.href = "/dashboard";
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
        console.error("Erro ao fazer login:", error);
        document.getElementById("erro").textContent = "Ocorreu um erro. Por favor, tente novamente mais tarde.";
    });
}

// Verificar se ele tem a mensagem do Sign Up,
// e se sim, mostra-la
const Message = sessionStorage.getItem("msg")
if (Message)
    {
    document.getElementById("erro").innerText = Message
    sessionStorage.removeItem("msg")
    }