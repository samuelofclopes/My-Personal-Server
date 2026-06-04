document.addEventListener("DOMContentLoaded", carregarMoral); // Assim que a pagina carregar, chamamos carregarMoral
document.addEventListener("DOMContentLoaded", carregarUpdates); // Assim que a pagina carregar, chamamos carregarUpdates
setInterval(carregarMoral, 25000); // A cada 25 segundos, chamamos carregarMoral para atualizar o mural sem precisar recarregar a página

function carregarMoral() {

    // Fazemos um fetch para a rota da API que retorna as mensagens do mural
    fetch("/api/moral")

        // Transformamos a resposta em JSON
        .then(response => response.json())

        // Agora 'data' é o objeto retornado pela API, que deve conter um array de mensagens
        .then(data => 
                {
                const m = document.getElementById("moral");
                m.innerText = ""; // Limpa o "Carregando..."

                // Pega cada mensagem do array de mensagens e adiciona ao mural
                data.mensagens.forEach(msg => 
                    {
                    const p = document.createElement("p");
                    p.innerText = msg.content;
                    p.innerHTML += "<br><span class='moral-info'>User: " + msg.user + " | Postado em: " + new Date(msg.created_at).toLocaleString()+ "</span>";
                    m.appendChild(p);
                    });
                })
            
            // Se ocorrer um erro ao carregar as mensagens, exibe uma mensagem de erro na consola e na página
            .catch(error => 
                    {
                        console.error("Erro ao carregar a moral:", error);
                    document.getElementById("moral").innerText = "Erro ao carregar mensagens.";
                    }
             );
}



function carregarUpdates() {
    fetch("/static/data/updates.json")

        // Transformamos a resposta em JSON
        .then(response => response.json())

        // Agora 'data' é o objeto retornado pelo JSON, que deve conter um array de updates
        .then(data =>
            {
            const u = document.getElementById("updates"); // Seleciona o elemento onde os updates serão exibidos
            u.innerText = ""; // Limpa o "A carregar..."
            data.updates.forEach(update => 
                { // Para cada update no array de updates adiciona o update
                u.innerHTML += `${update.type} - ${update.date} - ${update.title}<br><br>`;
                });
            })

        // Se ocorrer um erro ao carregar o JSON, exibe uma mensagem de erro na consola e na página
        .catch(error =>
            {
            console.error("Erro ao carregar os updates:", error);
            document.getElementById("updates").innerText = "Erro ao carregar updates.";
            });
            
}