# SolidárioMPL

SolidárioMPL é uma plataforma digital destinada a conectar doadores e beneficiários, facilitando a doação de itens essenciais e serviços para aqueles que precisam.

## Índice

- [Introdução](#introdução)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

## Introdução

SolidárioMPL é um projeto desenvolvido para ajudar na redistribuição de recursos para comunidades carentes. A plataforma permite que doadores registrem itens e serviços que desejam doar, e que beneficiários solicitem esses recursos de acordo com suas necessidades.
Este projecto foi criado por intermedio da MARIA DO NASCIMENTO uma aluna do INSTITUTO SUPERIOR POLITÉCNICO INTERNACIONAL DE ANGOLA na Faculdade de Engenharia Informática, para o projecto final do ano, a plataforma foi criada e desenvovildo por mim.

## Funcionalidades

- **Cadastro de usuários**: Permite que doadores e beneficiários se registrem na plataforma.
- **Registro de doações**: Doadores podem listar itens e serviços disponíveis para doação.
- **Solicitação de doações**: Beneficiários podem procurar e solicitar itens e serviços.
- **Gerenciamento de doações**: Administração de doações e solicitações para garantir a transparência e eficiência na distribuição.

## Instalação

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/GitHubJordan/solidarioMPL.git
    cd solidarioMPL
    ```

2. **Crie um ambiente virtual e ative-o**:
    ```bash
    python -m venv env
    source env/bin/activate  # No Windows, use `env\Scripts\activate`
    ```

3. **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure o banco de dados**:
    ```bash
    python manage.py migrate
    ```

5. **Crie um superusuário**:
    ```bash
    python manage.py createsuperuser
    ```

6. **Inicie o servidor de desenvolvimento**:
    ```bash
    python manage.py runserver
    ```

## Configuração

Antes de iniciar o servidor, você deve configurar as variáveis de ambiente necessárias. Crie um arquivo `.env` na raiz do projeto e adicione as seguintes configurações:

```env
SECRET_KEY=sua_chave_secreta
DEBUG=True
ALLOWED_HOSTS=127.0.0.1, .localhost
DATABASE_URL=postgres://user:password@localhost:5432/solidariompl
```

## Uso
1. Acesse a administração do Django: Navegue para http://127.0.0.1:8000/admin e faça login com as credenciais do superusuário.
2. Gerencie usuários, doações e solicitações através do painel administrativo.
3. Navegue pelo site principal para visualizar e interagir com a plataforma como um doador ou beneficiário.

## Contribuição
Se você quiser contribuir com o SolidárioMPL, siga os passos abaixo:

1. Fork o repositório.
2. Crie um branch para sua feature: git checkout -b minha-feature.
3. Faça commit das suas alterações: git commit -m 'Adicionar minha feature'.
4. Envie para o branch remoto: git push origin minha-feature.
5. Abra um Pull Request.

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Contato
Para mais informações, dúvidas ou sugestões, entre em contato:

Nome: Jordan Adelino
Email: jordan.adelino@exemplo.com
Telefone: +244 932 003 228
Facebook: https://www.facebook.com/jordan.adelino.98
Instagram: https://www.instagram.com/jordan_adelino
Twitter: https://www.twitter.com/adelino_jordan
Linkedn: https://www.linkedin.com/in/jordan-adelino

Obrigado por usar o SolidárioMPL! Juntos, podemos fazer a diferença.
