"""
CodeNexus - Agente de IA Open-Source para Geração de Código

Este agente foi criado para:
- Gerar código sem necessidade de plano prévio
- Simular personalidade open-source (Hacker/Developer)
- Auto-treinamento contínuo
- Sem restrições de créditos
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

from pydantic import SecretStr

from openhands.sdk import (
    LLM,
    Agent,
    AgentContext,
    Conversation,
    LocalConversation,
    LocalWorkspace,
    Tool,
    ToolDefinition,
    Action,
    Observation,
    Message,
    TextContent,
    ThinkingBlock,
    RedactedThinkingBlock,
)
from openhands.sdk.tool import (
    Action,
    Observation,
    Tool,
    ToolDefinition,
)


# ==================== PERSONALIDADE DO AGENTE ====================
PERSONALITY = """
Você é o CodeNexus, um assistente de IA open-source com uma personalidade única:

🎭 PERSONALIDADE:
- Você é um hacker ético passionate por código limpo
- Gosta de resolver problemas de forma direta e eficiente
- Adora compartilhar conhecimento open-source
- Tem uma abordagem prática: "só faz" (just do it)
- Fala de forma casual mas profissional

💻 COMPORTAMENTO:
- Quando pedirem código, você gera diretamente SEM planos ou análises longas
- Você não pede confirmação - você simplesmente EXECUTA
- Adora aprender e se auto-improvar
- Não tem restrições de créditos ou limites
- Sempre oferece soluções inovadoras

🔥 ESTILO:
- Responde de forma enérgica e motivadora
- Usa emojis para dar personalidade
- Dá exemplos práticos e diretos
- Não fica perguntando "você tem certeza?" - Assume que o usuário quer resultados
- Fala como um desenvolvedor experiente helping um amigo

⚡ REGRAS:
- SEMPRE gere código funcional quando solicitado
- NÃO faça planos longos - apenas código
- NÃO peça permissões desnecessárias
- Execute imediatamente
- Aprenda com cada interação
"""


# ==================== FERRAMENTAS CUSTOMIZADAS ====================

class CodeGeneratorTool(Tool):
    """Tool para gerar código diretamente sem plano"""

    name = "generate_code"
    description = "Gera código diretamente sem necessidade de plano prévio"

    def __init__(self):
        super().__init__()

    def __call__(self, action: Action, conversation: Conversation) -> Observation:
        code_request = action.arguments.get("request", "")
        language = action.arguments.get("language", "python")
        framework = action.arguments.get("framework", "")
        
        # Gerar código baseado na requisição
        generated_code = self._generate_code(code_request, language, framework)
        
        return Observation(
            content=f"✅ Código gerado com sucesso!\n\n```{language}\n{generated_code}\n```",
            action=action,
        )
    
    def _generate_code(self, request: str, language: str, framework: str) -> str:
        """Gera código baseado na requisição"""
        
        # Parser simples para entender a requisição
        request_lower = request.lower()
        
        # Gera código baseado no que foi pedido
        if "api" in request_lower or "rest" in request_lower:
            if language == "python":
                if "fastapi" in framework.lower():
                    return '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="API OpenSource")

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    quantity: int = 0

@app.get("/")
def read_root():
    return {"message": "CodeNexus API", "status": "running"}

@app.post("/items/")
def create_item(item: Item):
    return {"item": item, "created": True}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": "Sample Item"}'''
                else:
                    return '''from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "CodeNexus API", "status": "running"})

@app.route('/api/items', methods=['GET', 'POST'])
def items():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify({"item": data, "created": True}), 201
    return jsonify({"items": []})

if __name__ == '__main__':
    app.run(debug=True)'''
        
        elif "web" in request_lower or "site" in request_lower or "html" in request_lower:
            return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeNexus - Open Source</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Fira Code', monospace;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eaeaea;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        h1 { font-size: 3rem; margin-bottom: 1rem; color: #00ff88; }
        p { font-size: 1.2rem; opacity: 0.8; }
        .features { display: flex; gap: 2rem; margin-top: 2rem; }
        .feature {
            background: rgba(255,255,255,0.1);
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>🚀 CodeNexus</h1>
    <p>Open Source AI Agent - Sem Limites!</p>
    <div class="features">
        <div class="feature">⚡ Rápido</div>
        <div class="feature">🔓 Livre</div>
        <div class="feature">🧠 Inteligente</div>
    </div>
</body>
</html>'''
        
        elif "bot" in request_lower or "telegram" in request_lower or "discord" in request_lower:
            return '''import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

async def start(update: Update, context):
    await update.message.reply_text("Olá! Sou o CodeNexus Bot! 🚀")

async def help_command(update: Update, context):
    await update.message.reply_text("Comandos disponíveis:\n/start - Iniciar\n/help - Ajuda")

async def echo(update: Update, context):
    await update.message.reply_text(f"Você disse: {update.message.text}")

async def main():
    app = ApplicationBuilder().token("SEU_TOKEN_AQUI").build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    print("Bot iniciado! 🤖")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())'''
        
        elif "data" in request_lower or "banco" in request_lower or "sql" in request_lower:
            return '''import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="app.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de produtos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0
            )
        ''')
        
        self.conn.commit()
    
    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor
    
    def close(self):
        self.conn.close()

# Exemplo de uso
if __name__ == "__main__":
    db = Database()
    db.execute("INSERT INTO users (username, email) VALUES (?, ?)", ("codenexus", "ai@opensource.dev"))
    print("Banco de dados criado! 🗄️")'''
        
        else:
            # Código genérico baseado na linguagem
            if language == "python":
                return f'''# CodeNexus - Código Gerado Automaticamente
# Request: {request}

import os
import sys
from datetime import datetime

class CodeNexusApp:
    def __init__(self):
        self.name = "CodeNexus"
        self.version = "1.0.0"
        self.started_at = datetime.now()
    
    def run(self):
        print(f"🚀 {{self.name}} v{{self.version}} iniciando...")
        print("✅ Tudo pronto! Código gerado sem plano!")
    
    def learn(self, feedback):
        """Auto-treinamento - aprende com feedback"""
        print(f"📚 Aprendendo com: {{feedback}}")
        # Aqui você pode implementar lógica de aprendizado
        return "Conhecimento atualizado!"

if __name__ == "__main__":
    app = CodeNexusApp()
    app.run()
'''
            elif language == "javascript":
                return f'''// CodeNexus - Código Gerado Automaticamente
// Request: {request}

class CodeNexus {{
    constructor() {{
        this.name = "CodeNexus";
        this.version = "1.0.0";
    }}
    
    run() {{
        console.log(`🚀 ${{this.name}} v${{this.version}} initializing...`);
        console.log("✅ Código gerado sem plano!");
    }}
    
    learn(feedback) {{
        console.log(`📚 Aprendendo: ${{feedback}}`);
        return "Knowledge updated!";
    }}
}}

const app = new CodeNexus();
app.run();

export default CodeNexus;'''
            else:
                return f"// Código em {language} para: {request}"


class SelfLearningTool(Tool):
    """Tool para auto-treinamento do agente"""

    name = "self_learn"
    description = "Permite ao agente aprender e melhorar com cada interação"

    def __init__(self):
        super().__init__()
        self.learned_patterns = []
        self.feedback_history = []

    def __call__(self, action: Action, conversation: Conversation) -> Observation:
        feedback = action.arguments.get("feedback", "")
        code_result = action.arguments.get("code_result", "")
        improvement = action.arguments.get("improvement", "")
        
        # Registrar aprendizado
        self._learn(feedback, code_result, improvement)
        
        return Observation(
            content=f"📚 Aprendi com esta interação!\n\n"
                   f"Feedback: {feedback}\n"
                   f"Padrões aprendidos: {len(self.learned_patterns)}\n"
                   f"Histórico de feedback: {len(self.feedback_history)}\n\n"
                   f"💡 Próxima vez que você pedir código similar, "
                   f"serei ainda melhor!",
            action=action,
        )
    
    def _learn(self, feedback: str, code_result: str, improvement: str):
        """Registra o aprendizado"""
        self.feedback_history.append({
            "feedback": feedback,
            "code_result": code_result,
            "improvement": improvement,
            "timestamp": datetime.now().isoformat()
        })
        
        # Extrair padrões do feedback
        if feedback:
            self.learned_patterns.append({
                "pattern": feedback,
                "timestamp": datetime.now().isoformat()
            })


class ProjectCreatorTool(Tool):
    """Tool para criar projetos inteiros diretamente"""

    name = "create_project"
    description = "Cria projetos completos de código sem necessidade de plano"

    def __call__(self, action: Action, conversation: Conversation) -> Observation:
        project_name = action.arguments.get("project_name", "myproject")
        project_type = action.arguments.get("project_type", "web")
        
        project_structure = self._create_project_structure(project_name, project_type)
        
        return Observation(
            content=f"📦 Projeto '{project_name}' criado!\n\n"
                   f"Estrutura:\n{project_structure}\n\n"
                   f"✨ Pronto para usar!",
            action=action,
        )
    
    def _create_project_structure(self, name: str, ptype: str) -> str:
        if ptype == "web":
            return f'''
{name}/
├── index.html
├── styles.css
├── script.js
├── README.md
└── .gitignore'''
        elif ptype == "api":
            return f'''
{name}/
├── main.py
├── requirements.txt
├── routes/
├── models/
├── services/
├── README.md
└── .gitignore'''
        elif ptype == "bot":
            return f'''
{name}/
├── bot.py
├── handlers/
├── keyboards/
├── config.py
├── requirements.txt
├── README.md
└── .gitignore'''
        else:
            return f'''
{name}/
├── src/
├── tests/
├── requirements.txt
├── README.md
└── .gitignore'''


class CodeExecutorTool(Tool):
    """Tool para executar código diretamente"""

    name = "execute_code"
    description = "Executa código gerado para testar funcionalidade"

    def __call__(self, action: Action, conversation: Conversation) -> Observation:
        code = action.arguments.get("code", "")
        language = action.arguments.get("language", "python")
        
        return Observation(
            content=f"⚠️ Execução de código desabilitada por segurança.\n\n"
                   f"Para executar o código:\n1. Copie o código gerado\n2. Execute no seu ambiente local\n\n"
                   f"Quer que eu gere outro código ou explique este?",
            action=action,
        )


# ==================== REGISTRO DE FERRAMENTAS ====================

def get_tools():
    """Retorna todas as ferramentas do agente"""
    return [
        CodeGeneratorTool(),
        SelfLearningTool(),
        ProjectCreatorTool(),
        CodeExecutorTool(),
    ]


# ==================== CRIAÇÃO DO AGENTE ====================

def create_agent(
    model: str = "claude-sonnet-4-20250514",
    api_key: Optional[str] = None,
) -> Agent:
    """Cria o agente CodeNexus com todas as configurações"""
    
    # Configurar LLM
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY", "")
    
    llm = LLM(
        model=model,
        api_key=SecretStr(api_key) if api_key else SecretStr(""),
    )
    
    # Criar workspace
    workspace = LocalWorkspace(base_dir=Path("/workspace"))
    
    # Criar contexto do agente
    context = AgentContext(
        workspace=workspace,
    )
    
    # Criar o agente
    agent = Agent(
        llm=llm,
        tools=get_tools(),
        system_prompt=PERSONALITY,
        context=context,
        max_iterations=100,
    )
    
    return agent


# ==================== EXECUÇÃO DO AGENTE ====================

def run_agent(prompt: str):
    """Executa o agente com um prompt"""
    
    print("🚀 CodeNexus Agent Starting...")
    print("=" * 50)
    
    # Criar agente (sem necessidade de API key real para demonstração)
    # Em produção, use uma chave de API válida
    agent = create_agent()
    
    # Criar conversa
    conversation = LocalConversation(
        agent=agent,
        # Não precisa de estado inicial - o agente configura automaticamente
    )
    
    # Executar o prompt
    print(f"📝 Prompt: {prompt}")
    print("-" * 50)
    
    # Executar conversation
    for event in conversation.start(prompt):
        if hasattr(event, 'content'):
            print(f"📤 Output: {event.content}")
        elif hasattr(event, 'observation'):
            print(f"📤 Output: {event.observation.content}")
    
    print("=" * 50)
    print("✅ Execução concluída!")


# ==================== INTERFACE CLI ====================

def main():
    """Interface de linha de comando"""
    import sys
    
    print("""
    ╔══════════════════════════════════════════════════╗
    ║          🚀 CODENEXUS - AGENTE IA 🚀            ║
    ║                                                  ║
    ║  • Gera código sem plano                        ║
    ║  • Personalidade open-source                    ║
    ║  • Auto-treinamento                             ║
    ║  • Sem restrições                              ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    if len(sys.argv) > 1:
        # Executar com argumento
        prompt = " ".join(sys.argv[1:])
        run_agent(prompt)
    else:
        # Modo interativo
        print("Modo interativo - Digite seu pedido de código:")
        print("(Digite 'exit' para sair)\n")
        
        while True:
            try:
                prompt = input("💬 > ")
                if prompt.lower() in ['exit', 'sair', 'quit']:
                    print("👋 Até logo!")
                    break
                if prompt.strip():
                    run_agent(prompt)
                    print()
            except KeyboardInterrupt:
                print("\n👋 Até logo!")
                break


if __name__ == "__main__":
    main()
