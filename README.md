My-Personal-Server
============================================================================
Um servidor pessoal completo (Backend + Frontend), desenvolvido em Python com Flask — com autenticação JWT, verificação de email, recuperação de password e um mural de mensagens em tempo real.

Funcionalidades
============================================================================
-  Autenticação com JWT - (Token seguro, com verificação de email obrigatória antes do login)
-  Verificação de Email (2FA) - (Confirmação da conta via link enviado para o email do utilizador)
-  Recuperação de Password - (Fluxo completo de "Esqueci-me da password" via email)
-  Mural de Mensagens - (Os utilizadores autenticados podem postar e apagar comentários)
-  Controlo de permissões - (admin / Utilizador comum, para apagar comentários de outros)
-  Rate Limiting - (Limite de pedidos por IP em todas as rotas, com Flask-Limiter)
-  Validação de dados - (Username, Email e Password)
-  Envio de Emails Transacionais - (Via Resend, para verificação de conta e recuperação de password)
-  Status codes HTTP corretos - (400, 401, 403, 404...)
-  Frontend incluído - (Páginas de login, sign up, dashboard e perfil, em JavaScript puro)

Como usar?
============================================================================
Clonar o repositório
Criar um ambiente virtual
Instalar as dependências
Criar um ficheiro `.env` com as variáveis `DATABASE_URL`, `JWT_KEY` e `RESEND_KEY`
Executar a aplicação - (python3 main.py)
A API estará disponível em `http://localhost:5000`

FrontEnd
============================================================================
- `/` - Landing Page (com mural público e updates)
- `/signup` - Página de Sign Up
- `/login` - Página de Login
- `/dashboard` - Página principal after login (mural + updates)
- `/profile` - Página de perfil do utilizador
- `/forgot_password` - Pedido de recuperação de password
- `/reset_password` - Redefinição de password (acedida via link do email)

Endpoints
============================================================================
Autenticação
- POST /api/auth/signup - Registar novo utilizador (envia email de verificação)
- POST /api/auth/signin - Fazer login (retorna JWT token, requer email verificado)
- GET /api/auth/user - Ver dados do utilizador autenticado (requer token)
- GET /api/auth/confirm_email/<token> - Confirmar o email através do link enviado
- POST /api/auth/forgot_password - Pedir recuperação de password (envia email)
- GET/POST /api/auth/reset_password/<token> - Ver / submeter a nova password

Mural
- GET /api/moral - Listar as últimas 50 mensagens
- POST /api/moral/comentarios - Adicionar um comentário (requer token)
- DELETE /api/moral/comentarios/delete/<id> - Apagar um comentário (autor ou admin)

Porque eu o fiz?
===========================================================================

Este projeto é um dos projetos mais importantes que eu tenho, e tudo isso por um motivo simples, desafio, eu estava no 10º Ano do meu curso quando comecei a fazer este projeto, a materia de lá era simplesmente facil demais para mim, passei o ano inteiro a estudar coisas que eu já sabia quase de cór!
Por isso eu tive uma brilhante ideia, empenhar-me para fazer algo maior, um projeto realmente bom, e eu pensei "Ah, porque não um servidor?" e evoluindo as minhas ideias, este foi o resultado, no meu ver, foi um bom resultado, com direito a dominio, e tudo organizado, eu acho que este trabalho foi otimo 
para aprender como as coisas realmente funcionam, (Eu rodei este servidor por semanas seguidas, através de Termux, num telemovel reutilizado.)
O meu aprendizado ao longo de este projeto

Neste projeto adquiri varias competencias uteis, entre elas:
===========================================================================

- Flask Blueprints - (Organização das rotas em módulos separados: auth, moral, frontend)
- SQLAlchemy ORM - (Modelos `User` e `Message`, queries e relações)
- Flask-Migrate - (Gestão de migrações da base de dados)
- JWT (Flask-JWT-Extended) - (Autenticação stateless com tokens)
- itsdangerous - (Tokens temporizados e seguros para verificação de email e reset de password)
- Rate Limiting - (Flask-Limiter, a limitar pedidos por IP, inclusive atrás de um proxy Cloudflare)
- Envio de Emails Transacionais - (Integração com a API da Resend)
- Hashing de Passwords - (Werkzeug security)
- JavaScript puro (Vanilla JS) - (Fetch API, localStorage/sessionStorage, sem frameworks)
- Separação Backend/Frontend - (Mesmo o Flask a servir o HTML, toda a comunicação é feita via fetch para a API)
