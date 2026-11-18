// Carrega as três funções assim que a página é carregada
document.addEventListener("DOMContentLoaded", async () => {
    await ver_token();
    carregarMural();
    carregarUpdates();
});

// define um intervalo para atualizar a mural a cada 25 segundos
setInterval(carregarMural, 25000);

// Variável global para armazenar o utilizador atual
let utilizadorAtual = null;



// Função para verificar o token e obter os dados do utilizador
async function ver_token() 
    {
    const token = localStorage.getItem("token");

    try 
        {
        const resposta = await fetch("/api/auth/user", 
            {
            headers: { "Authorization": `Bearer ${token}` }
            });

        if (resposta.status === 401) 
            {
            localStorage.removeItem("token");
            window.location.href = "/login";
            return;
            }

        const dados = await resposta.json();
        utilizadorAtual = dados.user;

        }
        catch (error) 
            {
            console.error("Erro na conexão:", error);
            window.location.href = "/login";
            }
    }




// função para fazer logout
function logout() 
    {
    localStorage.removeItem("token");
    window.location.href = "/login";
    }




// Função para carregar as mensagens da mural
function carregarMural() 
    {
    
    // Fazer o FETCH para obter as mensagens da mural
    fetch("/api/mural")

        //Transformar a resposta em JSON
        .then(response => response.json())


        .then(data => 
            {
            // Limpar o container antes de adicionar as mensagens
            const container = document.getElementById("mural");
            container.innerHTML = "";

            
            // Adicionar cada mensagem ao container
            data.mensagens.forEach(msg => 
                {
                const div = document.createElement("div");
                div.className = "mural-msg";
                div.innerHTML = msg.content +
                    "<span class='mural-info'>User: " + msg.user +
                    " | Postado em: " + new Date(msg.created_at).toLocaleString() + "</span>";

                
                // se o utilizador atual for admin ou autor do comentário, mostrar o botão de apagar
                if (utilizadorAtual && (utilizadorAtual.is_admin || utilizadorAtual.username === msg.user)) 
                    {
                    const b = document.createElement("button");
                    b.innerText = "Delete";
                    b.className = "apagar_comentario_button";
                    b.onclick = () => apagarComentario(msg.id);
                    div.appendChild(b);
                    }

                container.appendChild(div);
                });
            })
        
        // Apanhamos o erro caso haja algum problema na conexão ou no processamento dos dados, e informamos o utilizador
        .catch(error => 
            {
            console.error("Erro ao carregar a mural:", error);
            document.getElementById("mural").innerText = "Erro ao carregar mensagens.";
            });
        }



// Função para apagar um comentário
function apagarComentario(id) 
    {
    fetch("/api/mural/comentarios/" + id, 
        {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
        })

    .then(response => 
        {
        if (response.ok) 
            {
            carregarMural();
            } 
        else 
            {
            console.error("Erro ao apagar comentário:", response.statusText);
            }
        })

    .catch(error => console.error("Erro na conexão:", error));
    }




// Função para enviar um comentário
function Comentar() 
    {
    const comentario = document.getElementById("comentario");


    // Verificar se o comentário não está vazio ou apenas com espaços
    if (!comentario.value.trim()) return; // .trim é como o .strip em python

    // Fazer o FETCH para enviar o comentário
    fetch("/api/mural/comentarios", 
        {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: JSON.stringify({ content: comentario.value })
    })

    // Se a resposta for bem-sucedida, limpar o campo de comentário e recarregar as mensagens da mural. Caso contrário, mostrar um erro no console.
    .then(response => 
        {
        if (response.ok) 
            {
            comentario.value = "";
            carregarMural();
            } 
        else 
            {
            console.error("Erro ao enviar comentário:", response.statusText);
        }
    })
    .catch(error => console.error("Erro na conexão:", error));
    }





// Função para carregar os updates
function carregarUpdates() 
    {
    // Fazer o FETCH para obter os updates
    fetch("/static/data/updates.json")
        .then(response => response.json())

        .then(data => 
            {
            const container = document.querySelector(".left_side_container h4");
            let html = '"The only way to do great work is to love what you do." - Steve Jobs<br><br>';
            
            // Para cada update, adicionar o tipo, data e título ao HTML
            data.updates.forEach(update => 
                {
                html += `${update.type} - ${update.date} - ${update.title}<br><br>`;
                });

            container.innerHTML = html;
            })
        
        // Apanhamos o erro caso haja algum problema na conexão ou no processamento dos dados, e informamos o utilizador
        .catch(error => console.error("Erro ao carregar updates:", error));
    }

// Função para redirecionar para a página de perfil
function ver_perfil() 
    {
    window.location.href = "/profile";
    }



// Adiciona um evento para enviar o comentário ao pressionar Enter
document.getElementById("comentario").addEventListener("keydown", function(event) 
    {
    if (event.key === "Enter" && !event.shiftKey) 
        {
        event.preventDefault();
        Comentar();
        }
    });