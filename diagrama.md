# ServiConnect - Diagrama de Classes UML (modelo GetNinja)

## Diagrama Completo

```mermaid
classDiagram
    class Usuario {
        +int id
        +String nome
        +String email
        +String cpf
        +String telefone
        +String senha
        +String cidade
        +String tipo
        +register()
        +login()
        +logout()
        +atualizarPerfil()
        +deletarConta()
    }

    class GoogleAuth {
        +String client_id
        +String client_secret
        +String redirect_uri
        +autenticar()
        +callback()
        +extrairDadosUsuario()
    }

    class Sessao {
        +String session_id
        +int user_id
        +String user_nome
        +String categoria
        +criarSessao()
        +destruirSessao()
        +renovarToken()
    }

    class Cliente {
        +String preferencias
        +listarSolicitacoes()
        +criarSolicitacao()
        +aceitarProposta()
        +avaliarProfissional()
        +historicoServicos()
    }

    class Profissional {
        +Double notaMedia
        +int totalAvaliacoes
        +List~String~ categorias
        +bool verificado
        +cadastrarCategorias()
        +enviarProposta()
        +avaliarCliente()
        +portfolio()
    }

    class Categoria {
        +int id
        +String nome
        +String descricao
        +int qtdProfissionais
    }

    class SolicitacaoServico {
        +int id
        +String descricao
        +String endereco
        +String status
        +Date dataCriacao
        +Date dataExecucao
        +Double orcamento
        +criar()
        +editar()
        +cancelar()
        +concluir()
        +listarPropostas()
    }

    class Proposta {
        +int id
        +Double preco
        +String descricao
        +String status
        +Date dataEnvio
        +enviar()
        +cancelar()
        +aceitar()
        +recusar()
    }

    class ServicoContratado {
        +int id
        +Date dataInicio
        +Date dataFim
        +Double valorFinal
        +String status
        +iniciar()
        +finalizar()
        +registrarPagamento()
    }

    class Avaliacao {
        +int id
        +int nota
        +String comentario
        +Date data
        +criar()
        +editar()
        +excluir()
        +calcularMedia()
    }

    class DBMySQL {
        +String host
        +String database
        +String user
        +String password
        +conectar()
        +desconectar()
        +executarQuery()
    }

    class LandingPage {
        +HeroSection
        +StatsSection
        +CategoriasGrid
        +VantagensSection
        +DepoimentosSection
        +CTASection
        +Footer
    }

    class FormLogin {
        +validarEmail()
        +toggleSenha()
        +submit()
    }

    class FormCadastro {
        +validarEmail()
        +validarCPF()
        +verificarForcaSenha()
        +mascaraCPF()
        +submit()
    }

    class PainelCliente {
        +verSolicitacoes()
        +verPropostas()
        +aceitarProposta()
        +avaliarProfissional()
    }

    class PainelProfissional {
        +verOportunidades()
        +enviarProposta()
        +verServicosAtivos()
        +avaliarCliente()
    }

    Usuario <|-- Cliente
    Usuario <|-- Profissional
    Usuario "1" --> "1" Sessao : possui
    GoogleAuth ..> Usuario : cria ou recupera
    Profissional "*" --> "*" Categoria : atua_em

    Cliente "1" --> "*" SolicitacaoServico : cria
    Profissional "1" --> "*" Proposta : envia

    SolicitacaoServico "1" --> "*" Proposta : recebe
    SolicitacaoServico "1" --> "0..1" ServicoContratado : gera

    Cliente "1" --> "*" Avaliacao : faz_sobre
    Profissional "1" --> "*" Avaliacao : recebe
    Avaliacao --> Profissional : impacta_nota

    FormLogin ..> Sessao : cria
    FormCadastro ..> Usuario : cria
    LandingPage --> FormCadastro : redireciona
    FormLogin ..> GoogleAuth : pode_usar

    Usuario ..> DBMySQL : usa
    SolicitacaoServico ..> DBMySQL : usa
    Proposta ..> DBMySQL : usa
    Avaliacao ..> DBMySQL : usa
```

## Legenda

| Relação | Símbolo | Significado |
|---------|---------|-------------|
| Herança | `Cliente → Usuario` | Cliente herda de Usuario |
| Composição | `"1" → "*" ` | Um para muitos |
| Dependência | `..>` | Usa/depende de |

## Descrição dos Pacotes

### Autenticação
- **Usuario** entidade central com dados pessoais e credenciais
- **GoogleAuth** implementa OAuth 2.0 para login via Google
- **Sessao** mantem o estado da sessão do usuário logado

### Usuários
- **Cliente** solicita serviços e avalia profissionais
- **Profissional** envia propostas e recebe avaliações
- **Categoria** agrupa profissionais por especialidade

### Serviços
- **SolicitacaoServico** criada pelo cliente com descrição e endereço
- **Proposta** enviada pelo profissional em resposta à solicitação
- **ServicoContratado** gerado quando proposta é aceita

### Avaliação
- **Avaliacao** conecta cliente e profissional com nota e comentário

### Frontend
- **LandingPage** página principal com hero, stats, categorias, depoimentos
- **FormLogin / FormCadastro** formulários com validação JS
- **PainelCliente / PainelProfissional** dashboards pós-login
