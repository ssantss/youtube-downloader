.PHONY: install run kill clean help

# Variables
BACKEND_DIR=backend
VENV_NAME=venv
PYTHON=python3
PIP=venv/bin/pip
VENV_ACTIVATE=. venv/bin/activate

help:
	@echo "Comandos disponibles:"
	@echo "  make install    - Instala todas las dependencias"
	@echo "  make kill      - Mata los procesos de backend y frontend"
	@echo "  make run       - Inicia frontend y backend"
	@echo "  make clean     - Limpia archivos temporales"

install-backend:
	@echo "🚀 Instalando dependencias del backend..."
	cd $(BACKEND_DIR) && $(PYTHON) -m venv $(VENV_NAME)
	cd $(BACKEND_DIR) && $(PIP) install -r requirements.txt --quiet

install-frontend:
	@echo "🚀 Instalando dependencias del frontend..."
	cd frontend && npm install

install: install-backend install-frontend
	@echo "✅ Instalación completada"

kill:
	@echo "🛑 Matando procesos anteriores..."
	@-lsof -ti:5270 | xargs kill -9 2>/dev/null || true
	@-lsof -ti:8765 | xargs kill -9 2>/dev/null || true
	@-pkill -f "python3 .*/main.py" 2>/dev/null || true
	@-pkill -f "vite" 2>/dev/null || true
	@sleep 1
	@echo "✅ Procesos detenidos"

run: kill
	@echo "🚀 Iniciando servicios..."
	cd $(BACKEND_DIR) && $(VENV_ACTIVATE) && $(PYTHON) main.py &
	cd frontend && npm run dev &
	@echo "✅ Servicios iniciados en:"
	@echo "📝 Frontend: Ok"
	@echo "📝 Backend: Ok"
	@trap 'make kill' INT; wait

clean:
	@echo "🧹 Limpiando archivos temporales..."
	make kill
	rm -rf $(BACKEND_DIR)/$(VENV_NAME)
	rm -rf frontend/node_modules
	rm -rf **/__pycache__
	@echo "✅ Limpieza completada" 