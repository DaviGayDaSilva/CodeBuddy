#!/usr/bin/env python3
"""
CodeNexus Agent - Debian Package (DEB)
Versão desktop para sistemas Debian/Ubuntu
"""

# ==================== METADADOS DO PACOTE ====================
PACKAGE_NAME = "codenexus"
PACKAGE_VERSION = "1.0.0"
PACKAGE_DESCRIPTION = "AI Agent para geração de código - Sem planos, sem limites"
PACKAGE_MAINTAINER = "CodeNexus Team"
PACKAGE_SECTION = "devel"
PACKAGE_PRIORITY = "optional"
PACKAGE_ARCHITECTURE = "all"
HOMEPAGE = "https://github.com/codenexus/codenexus-agent"

# ==================== ARQUIVOS DO PACOTE ====================
# Estes arquivos serão incluídos no DEB
PACKAGE_FILES = [
    ("usr/bin/codenexus", "codenexus_agent.py"),
    ("usr/share/doc/codenexus/copyright", "LICENSE"),
    ("usr/share/doc/codenexus/changelog.gz", "CHANGELOG.gz"),
    ("etc/codenexus/config.yaml", "config.yaml"),
]

# ==================== SCRIPT DE INSTALAÇÃO ====================
POSTINST_SCRIPT = """#!/bin/sh
# Script pós-instalação

# Criar diretório do usuário
mkdir -p ~/.codenexus

# Definir permissões
chmod +x /usr/bin/codenexus

echo "CodeNexus instalado com sucesso! 🚀"
echo "Execute: codenexus --help"

exit 0
"""

PRERM_SCRIPT = """#!/bin/sh
# Script pré-remoção

echo "Removendo CodeNexus..."

exit 0
"""


# ==================== INSTALADOR SIMPLES ====================

import os
import sys
import shutil
import subprocess


def install_deb():
    """Instala o CodeNexus no sistema"""
    
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║       📦 Instalando CodeNexus (DEB)              ║
    ╚═══════════════════════════════════════════════════╝
    """)
    
    # Verificar se é root
    if os.geteuid() != 0:
        print("⚠️  Execute como root: sudo python3 install_deb.py")
        return False
    
    try:
        # Criar diretórios
        print("📁 Criando diretórios...")
        os.makedirs("/usr/bin", exist_ok=True)
        os.makedirs("/usr/share/codenexus", exist_ok=True)
        os.makedirs("/usr/share/doc/codenexus", exist_ok=True)
        os.makedirs("/etc/codenexus", exist_ok=True)
        os.makedirs("/var/lib/codenexus", exist_ok=True)
        
        # Copiar arquivos principais
        print("📄 Copiando arquivos...")
        
        # Copiar agente principal
        if os.path.exists("/workspace/project/codenexus_agent.py"):
            shutil.copy("/workspace/project/codenexus_agent.py", "/usr/share/codenexus/agent.py")
            shutil.copy("/workspace/project/codenexus_agent.py", "/usr/bin/codenexus")
            os.chmod("/usr/bin/codenexus", 0o755)
        
        # Copiar exemplos
        if os.path.exists("/workspace/project/examples.py"):
            shutil.copy("/workspace/project/examples.py", "/usr/share/codenexus/examples.py")
        
        # Criar configuração padrão
        print("⚙️  Criando configuração...")
        config = """# CodeNexus Configuration
model: claude-sonnet-4-20250514
api_key: ""
max_iterations: 100
auto_learn: true

# Personalidade
personality:
  name: CodeNexus
  style: hacker
  language: pt-BR

# Logging
logging:
  level: INFO
  file: /var/log/codenexus.log
"""
        with open("/etc/codenexus/config.yaml", "w") as f:
            f.write(config)
        
        # Criar launcher
        launcher = """#!/bin/bash
# Launcher para CodeNexus

cd /usr/share/codenexus
exec python3 agent.py "$@"
"""
        with open("/usr/bin/codenexus", "w") as f:
            f.write(launcher)
        os.chmod("/usr/bin/codenexus", 0o755)
        
        # Criar documentação
        print("📚 Criando documentação...")
        
        license_text = """MIT License

Copyright (c) 2024 CodeNexus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        with open("/usr/share/doc/codenexus/copyright", "w") as f:
            f.write(license_text)
        
        changelog = """codenexus (1.0.0) stable; urgency=low

  * Initial release
  * AI code generation without plans
  * Open-source personality
  * Self-learning capability

 -- CodeNexus Team <team@codenexus.dev>  Mon, 02 Mar 2026 00:00:00 +0000
"""
        with open("/usr/share/doc/codenexus/changelog", "w") as f:
            f.write(changelog)
        
        # Compactar changelog
        try:
            import gzip
            with gzip.open("/usr/share/doc/codenexus/changelog.gz", "wt") as f:
                f.write(changelog)
        except:
            pass
        
        print("""
╔═══════════════════════════════════════════════════╗
║       ✅ Instalação concluída!                    ║
╚═══════════════════════════════════════════════════╝

🚀 Como usar:

  • Código rápido:
    $ codenexus "Crie uma API"

  • Modo interativo:
    $ codenexus

  • Ajuda:
    $ codenexus --help

📁 Arquivos instalados:
  • /usr/bin/codenexus
  • /usr/share/codenexus/
  • /etc/codenexus/config.yaml

""")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante instalação: {e}")
        return False


def uninstall_deb():
    """Desinstala o CodeNexus"""
    
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║       🗑️  Removendo CodeNexus                    ║
    ╚═══════════════════════════════════════════════════╝
    """)
    
    if os.geteuid() != 0:
        print("⚠️  Execute como root: sudo python3 install_deb.py --uninstall")
        return False
    
    try:
        # Remover arquivos
        if os.path.exists("/usr/bin/codenexus"):
            os.remove("/usr/bin/codenexus")
        
        if os.path.exists("/usr/share/codenexus"):
            shutil.rmtree("/usr/share/codenexus")
        
        if os.path.exists("/etc/codenexus"):
            shutil.rmtree("/etc/codenexus")
        
        if os.path.exists("/var/lib/codenexus"):
            shutil.rmtree("/var/lib/codenexus")
        
        print("✅ CodeNexus removido com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante remoção: {e}")
        return False


def create_deb_package():
    """Cria o pacote .deb (requer ferramentas de build)"""
    
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║       📦 Criando pacote .deb                     ║
    ╚═══════════════════════════════════════════════════╝
    """)
    
    # Verificar ferramentas
    try:
        subprocess.run(["dpkg-deb", "--version"], check=True, capture_output=True)
    except:
        print("⚠️  dpkg-deb não encontrado. Instale com:")
        print("    sudo apt install dpkg-dev")
        return False
    
    import tempfile
    import tarfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Criar estrutura
        pkg_dir = os.path.join(tmpdir, "codenexus-1.0.0")
        os.makedirs(pkg_dir)
        
        # DEBIAN directory
        debian_dir = os.path.join(pkg_dir, "DEBIAN")
        os.makedirs(debian_dir)
        
        # control file
        control = f"""Package: codenexus
Version: 1.0.0
Section: {PACKAGE_SECTION}
Priority: {PACKAGE_PRIORITY}
Architecture: {PACKAGE_ARCHITECTURE}
Maintainer: {PACKAGE_MAINTAINER}
Description: {PACKAGE_DESCRIPTION}
Homepage: {HOMEPAGE}
"""
        with open(os.path.join(debian_dir, "control"), "w") as f:
            f.write(control)
        
        # scripts
        with open(os.path.join(debian_dir, "postinst"), "w") as f:
            f.write(POSTINST_SCRIPT)
        os.chmod(os.path.join(debian_dir, "postinst"), 0o755)
        
        with open(os.path.join(debian_dir, "prerm"), "w") as f:
            f.write(PRERM_SCRIPT)
        os.chmod(os.path.join(debian_dir, "prerm"), 0o755)
        
        # Usr files
        os.makedirs(os.path.join(pkg_dir, "usr/bin"))
        os.makedirs(os.path.join(pkg_dir, "usr/share/codenexus"))
        
        # Copiar arquivos
        if os.path.exists("/workspace/project/codenexus_agent.py"):
            shutil.copy("/workspace/project/codenexus_agent.py", 
                       os.path.join(pkg_dir, "usr/share/codenexus/agent.py"))
        
        # Launcher
        launcher = """#!/bin/bash
cd /usr/share/codenexus
exec python3 agent.py "$@"
"""
        with open(os.path.join(pkg_dir, "usr/bin/codenexus"), "w") as f:
            f.write(launcher)
        os.chmod(os.path.join(pkg_dir, "usr/bin/codenexus"), 0o755)
        
        # Build
        deb_path = "/workspace/project/codenexus_1.0.0_all.deb"
        result = subprocess.run(
            ["dpkg-deb", "--build", pkg_dir, deb_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Pacote criado: {deb_path}")
            return True
        else:
            print(f"❌ Erro: {result.stderr}")
            return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--uninstall":
        uninstall_deb()
    elif len(sys.argv) > 1 and sys.argv[1] == "--build":
        create_deb_package()
    else:
        install_deb()
