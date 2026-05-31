function fazer_signup() {

    // Obter os valores dos campos de username e senha
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const email = document.getElementById("email").value;
    const confirm_password = document.getElementById("confirm_password").value;
    // Fazer o FECTH
    fetch("/api/auth/signup",
            {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ username, password, email, confirm_password })
            }
        )

    // Transformar a resposta em JSON
    .then(response => response.json())


    // Verificar se o login foi bem-sucedido
    .then(data =>
            {
            if (data.user) // Se o token existir, o login foi bem-sucedido, e guardamos o token e redirecionamos login
                {
                sessionStorage.setItem("msg", "Verifique a sua caixa de entrada para efetuar o login."); // Guardamos a mensagem para o login
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
        console.error("Erro ao fazer login:", error);
        document.getElementById("erro").textContent = "Ocorreu um erro. Por favor, tente novamente mais tarde.";
    });
}