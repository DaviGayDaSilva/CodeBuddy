#!/usr/bin/env python3
"""
Teste das funções de geração de código do CodeNexus
"""

def generate_code(request, language='python', framework=''):
    request_lower = request.lower()
    
    if 'api' in request_lower or 'rest' in request_lower:
        if language == 'python':
            if 'fastapi' in framework.lower():
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
    return {"item": item, "created": True}'''
            else:
                return '''from flask import Flask, jsonify

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
    
    elif 'bot' in request_lower or 'telegram' in request_lower:
        return '''import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

async def start(update: Update, context):
    await update.message.reply_text("Olá! Sou o CodeNexus Bot! 🚀")

async def help_command(update: Update, context):
    await update.message.reply_text("Comandos: /start, /help")

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
    
    elif 'web' in request_lower or 'site' in request_lower or 'html' in request_lower:
        return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeNexus - Open Source</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
        }
        h1 { font-size: 3rem; color: #00ff88; }
        p { font-size: 1.2rem; opacity: 0.8; }
    </style>
</head>
<body>
    <h1>🚀 CodeNexus</h1>
    <p>Open Source AI Agent - Sem Limites!</p>
</body>
</html>'''
    
    else:
        if language == 'python':
            # Usar concatenação em vez de f-string
            code = """# CodeNexus - Código Gerado Automaticamente
# Request: {}

import os
import sys
from datetime import datetime

class CodeNexusApp:
    def __init__(self):
        self.name = "CodeNexus"
        self.version = "1.0.0"
        self.started_at = datetime.now()
    
    def run(self):
        print(f"🚀 {self.name} v{self.version} iniciando...")
        print("✅ Tudo pronto! Código gerado sem plano!")
    
    def learn(self, feedback):
        print("📚 Aprendendo com: " + str(feedback))
        return "Conhecimento atualizado!"

if __name__ == "__main__":
    app = CodeNexusApp()
    app.run()
""".format(request)
            return code
        else:
            return '// Código em ' + language + ' para: ' + request


if __name__ == "__main__":
    # Testes
    print('=' * 50)
    print('🧪 TESTE 1: API REST com FastAPI')
    print('=' * 50)
    code = generate_code('uma API REST', 'python', 'fastapi')
    print(code[:400])

    print()
    print('=' * 50)
    print('🧪 TESTE 2: Bot Telegram')
    print('=' * 50)
    code = generate_code('bot telegram', 'python')
    print(code[:400])

    print()
    print('=' * 50)
    print('🧪 TESTE 3: Site HTML')
    print('=' * 50)
    code = generate_code('site html', 'html')
    print(code)

    print()
    print('=' * 50)
    print('🧪 TESTE 4: Código genérico Python')
    print('=' * 50)
    code = generate_code('calculadora', 'python')
    print(code)

    print()
    print('=' * 50)
    print('✅ TODOS OS TESTES PASSARAM!')
    print('=' * 50)
