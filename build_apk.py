#!/usr/bin/env python3
"""
CodeNexus Agent - Build APK Script
Script para compilar o app para Android (APK)
"""

import os
import sys
import subprocess


def build_apk():
    """Compila o app para Android usando Flet"""
    
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║       📱 Compilando CodeNexus APK                ║
    ╚═══════════════════════════════════════════════════╝
    """)
    
    # Verificar se Flet está instalado
    try:
        import flet
        print(f"✅ Flet encontrado: {flet.__version__}")
    except ImportError:
        print("❌ Flet não está instalado!")
        print("   Execute: pip install flet")
        return False
    
    # Verificar arquivos necessários
    if not os.path.exists("/workspace/project/codenexus_apk.py"):
        print("❌ Arquivo codenexus_apk.py não encontrado!")
        return False
    
    print("""
📋 Preparando build para Android...

O Flet pode criar apps para:
  • Android (APK) - Requer Android SDK
  • iOS (IPA) - Requer macOS e Xcode
  • Web (HTML5)
  • Desktop (Windows, macOS, Linux)

Para compilar o APK, você precisa de:

1. Android SDK instalado
2. Variáveis de ambiente configuradas:
   - ANDROID_HOME ou ANDROID_SDK_ROOT
3. Java JDK 11+

Alternativamente, você pode usar o build remoto do Flet:
""")
    
    # Criar arquivo de спецификации para build
    spec_content = """
[project]
name = codenexus
version = 1.0.0
description = CodeNexus AI Agent - Gerador de Código
author = CodeNexus Team

[project.urls]
Homepage = https://github.com/codenexus

[build]
prebuild = false
""" + """
"""
    
    with open("/workspace/project/codenexus.spec", "w") as f:
        f.write(spec_content)
    
    print("""
📝 Opções de Build:

A) BUILD LOCAL (requer Android SDK):
   
   1. Instale o Android SDK:
      https://developer.android.com/studio
   
   2. Configure as variáveis:
      export ANDROID_HOME=/path/to/android/sdk
      export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
   
   3. Execute:
      flet build apk --project /workspace/project

B) BUILD REMOTO (simplificado):
   
   Use o GitHub Actions ou serviço de build automático

C) TESTAR EMULADOR:
   
   flet run --android /workspace/project/codenexus_apk.py

D) TESTAR WEB:
   
   flet run /workspace/project/codenexus_apk.py --web

""")
    
    # Tentar build local
    print("\n🔨 Tentando build local...")
    
    try:
        # Verificar Android SDK
        android_home = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
        
        if android_home:
            print(f"✅ Android SDK: {android_home}")
            
            # Executar build
            result = subprocess.run(
                ["flet", "build", "apk", "--project", "/workspace/project", 
                 "--output", "/workspace/project/codenexus.apk"],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print("✅ APK compilado com sucesso!")
                print("📁 Output: /workspace/project/codenexus.apk")
                return True
            else:
                print(f"⚠️  Build local falhou: {result.stderr}")
        else:
            print("⚠️  Android SDK não encontrado")
            
    except FileNotFoundError:
        print("⚠️  Comando 'flet' não encontrado no PATH")
    except Exception as e:
        print(f"⚠️  Erro: {e}")
    
    # Criar instruções detalhadas
    create_build_instructions()
    
    return False


def create_build_instructions():
    """Cria instruções detalhadas de build"""
    
    instructions = """# CodeNexus APK Build Instructions

## Requisitos

### Linux (Debian/Ubuntu)

```bash
# 1. Instalar dependências
sudo apt update
sudo apt install -y openjdk-17-jdk wget unzip

# 2. Baixar Android SDK
mkdir -p ~/android-sdk/cmdline-tools
cd ~/android-sdk/cmdline-tools
wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
unzip commandlinetools-linux-11076708_latest.zip
mv cmdline-tools latest

# 3. Configurar ambiente
export ANDROID_HOME=~/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# 4. Aceitar licenças
yes | sdkmanager --licenses

# 5. Instalar componentes
sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"

# 6. Compilar APK
cd /workspace/project
flet build apk --project . --output codenexus.apk
```

### macOS

```bash
# 1. Instalar Java
brew install openjdk@17

# 2. Baixar Android Studio
# https://developer.android.com/studio

# 3. Configurar variáveis
export ANDROID_HOME=~/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin

# 4. Compilar
flet build apk --project . --output codenexus.apk
```

### Windows

```powershell
# 1. Instalar Java JDK 17
# https://adoptium.net/

# 2. Baixar Android SDK Command Line Tools
# https://developer.android.com/studio#command-line-tools

# 3. Configurar variáveis de ambiente
$env:ANDROID_HOME = "C:\\Android\\sdk"
$env:PATH += ";$env:ANDROID_HOME\\cmdline-tools\\latest\\bin"

# 4. Compilar
flet build apk --project . --output codenexus.apk
```

## Usando Docker (Alternativa)

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget unzip openjdk-17-jdk

# Android SDK
ENV ANDROID_HOME=/root/android-sdk
RUN wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O /tmp/cmdtools.zip && \
    mkdir -p $ANDROID_HOME/cmdline-tools && \
    unzip -q /tmp/cmdtools.zip -d $ANDROID_HOME/cmdline-tools && \
    mv $ANDROID_HOME/cmdline-tools/cmdline-tools $ANDROID_HOME/cmdline-tools/latest

ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

RUN yes | sdkmanager --licenses || true
RUN sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"

# Flet
RUN pip install flet

WORKDIR /app
COPY . .

CMD ["flet", "build", "apk", "--project", ".", "--output", "codenexus.apk"]
```

## Build Automático com GitHub Actions

```yaml
name: Build APK

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Setup Android SDK
        uses: android-actions/setup-android@v2
      
      - name: Install Flet
        run: pip install flet
      
      - name: Build APK
        run: flet build apk --project . --output codenexus.apk
      
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: codenexus-apk
          path: codenexus.apk
```

## Instalando o APK no Android

```bash
# Conectar dispositivo
adb devices

# Instalar APK
adb install codenexus.apk

# Reinstalar (preservar dados)
adb install -r codenexus.apk
```

## Build Web (Alternativa Sem Android SDK)

Se você não puder instalar o Android SDK, pode fazer build para Web:

```bash
flet build web --project /workspace/project --output /workspace/project/web-build
```

Depois, hospede os arquivos em qualquer servidor web.
"""
    
    with open("/workspace/project/BUILD_INSTRUCTIONS.md", "w") as f:
        f.write(instructions)
    
    print("📄 Instruções detalhadas salvas em: BUILD_INSTRUCTIONS.md")


if __name__ == "__main__":
    success = build_apk()
    sys.exit(0 if success else 1)
