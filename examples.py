"""
Exemplos de uso do CodeNexus Agent

Este arquivo demonstra como usar o agente de IA CodeNexus para:
- Gerar código sem necessidade de plano
- Criar projetos completos
- Auto-treinamento
"""

# ==================== EXEMPLO 1: Gerar API ====================
"""
prompt = "Crie uma API REST com FastAPI para gerenciar tarefas"
# Resultado: API completa com endpoints para CRUD de tarefas
"""


# ==================== EXEMPLO 2: Gerar Bot Telegram ====================
"""
prompt = "Crie um bot do Telegram que responde mensagens"
# Resultado: Bot completo com handlers para mensagens
"""


# ==================== EXEMPLO 3: Criar Projeto Web ====================
"""
from codenexus_agent import run_agent

# Criar projeto web completo
run_agent("Crie um projeto web com HTML, CSS e JS")

# Resultado:
# myproject/
# ├── index.html
# ├── styles.css
# ├── script.js
# └── README.md
"""


# ==================== EXEMPLO 4: Auto-Treinamento ====================
"""
# O agente aprende automaticamente com cada interação
# Após receber feedback, ele melhora para próximas gerações

# Exemplo de feedback:
feedback = "O código poderia usar async/await"
improvement = "Sempre use async/await para operações assíncronas"

# O agente registra isso e aplica em códigos futuros
"""


# ==================== EXEMPLO 5: Uso Avançado ====================
"""
from codenexus_agent import create_agent, LocalConversation

# Criar agente com configurações personalizadas
agent = create_agent(
    model="claude-sonnet-4-20250514",  # Modelo desejado
    api_key="sua-api-key-aqui"  # Sua chave de API
)

# Criar conversa
conversation = LocalConversation(agent=agent)

# Executar múltiplos prompts na mesma sessão
prompts = [
    "Crie uma função para calcular Fibonacci",
    "Agora adicione cache memoization",
    "Transforme em uma classe",
]

for prompt in prompts:
    for event in conversation.start(prompt):
        print(event.content)
"""


# ==================== EXEMPLO 6: Integração com CLI ====================
"""
# Execute o agente diretamente do terminal:

# python codenexus_agent.py "Crie uma calculadora em Python"

# Ou entre no modo interativo:
# python codenexus_agent.py
"""


# ==================== PERSONALIDADE DO AGENTE ====================
"""
O CodeNexus tem uma personalidade única:

- 🎯 FOCO: Gera código diretamente, sem planos longos
- 🚀 VELOCIDADE: Execução rápida e eficiente  
- 🔓 OPEN-SOURCE: Gosta de compartilhar conhecimento
- 🧠 INTELIGENTE: Aprende com cada interação
- 💪 SEM LIMITES: Sem restrições de créditos

Quando você pede código, ele:
1. Entende a requisição
2. Gera código funcional imediatamente
3. Oferece explicações se necessário
4. Aprende com seu feedback para melhorar
"""


# ==================== FERRAMENTAS DISPONÍVEIS ====================
"""
O agente possui 4 ferramentas principais:

1. generate_code - Gera código em qualquer linguagem
   - Parâmetros: request, language, framework
   - Exemplo: generate_code(request="API REST", language="python", framework="fastapi")

2. self_learn - Aprende com feedback
   - Parâmetros: feedback, code_result, improvement
   - Exemplo: self_learn(feedback="Use async", improvement="Sempre usar async/await")

3. create_project - Cria estrutura de projeto completa
   - Parâmetros: project_name, project_type
   - Exemplo: create_project(project_name="myapp", project_type="web")

4. execute_code - Executa código (desabilitado por segurança)
   - Parâmetros: code, language
   - Exemplo: execute_code(code="print('hello')", language="python")
"""


# ==================== TESTE RÁPIDO ====================
if __name__ == "__main__":
    print(__doc__)
    
    # Teste das ferramentas
    from codenexus_agent import (
        CodeGeneratorTool,
        SelfLearningTool,
        ProjectCreatorTool,
    )
    from openhands.sdk.tool import Action
    
    print("\n=== Teste: CodeGeneratorTool ===")
    tool = CodeGeneratorTool()
    action = Action(
        tool_name="generate_code",
        arguments={"request": "uma API REST", "language": "python", "framework": "fastapi"}
    )
    obs = tool(action, None)
    print(obs.content[:500] + "...")
    
    print("\n=== Teste: SelfLearningTool ===")
    tool = SelfLearningTool()
    action = Action(
        tool_name="self_learn",
        arguments={
            "feedback": "Use type hints",
            "code_result": "def func(x): return x",
            "improvement": "Sempre usar type hints"
        }
    )
    obs = tool(action, None)
    print(obs.content)
    
    print("\n=== Teste: ProjectCreatorTool ===")
    tool = ProjectCreatorTool()
    action = Action(
        tool_name="create_project",
        arguments={"project_name": "myapi", "project_type": "api"}
    )
    obs = tool(action, None)
    print(obs.content)
    
    print("\n✅ Todos os testes passaram!")
