# SistemaRefacciónExperto

Sistema de selección de refacciones guatemaltecas V.1

---

# 🚀 Guía para Crear y Subir tu Rama al Proyecto

Para mantener el proyecto organizado y evitar conflictos con el código de los demás, cada miembro del equipo debe trabajar en su propia rama. Sigue estos pasos en tu terminal:

### 0. Clona el repositorio
```bash
git clone https://github.com/LuisAlfred1/sistemas-expertos-proyecto.git
```

### 1. Actualizar el repositorio local
Antes de crear una rama, asegúrate de tener la última versión del código de la rama principal (`main` o `master`).
```bash
git checkout main
git pull origin main
```

### 2. Crear y cambiar a tu nueva rama
Crea tu rama usando tu nombre.
```bash
git checkout -b tu-nombre-de-rama
```

### 3. Trabajar en tus cambios y guardarlos
Realiza los cambios necesarios en tu editor de código. Cuando termines una parte, guarda tu progreso:
```bash
# Agregar los archivos al escenario
git add .

# Confirmar los cambios con un mensaje descriptivo
git commit -m "feat: descripción corta de lo que agregaste"
```

### 4. Subir la rama a GitHub
La **primera vez** que subas tu rama, debes enlazarla con el servidor remoto usando este comando:
```bash
git push -u origin tu-nombre-de-rama
```
*A partir de la segunda vez que subas cambios en esta misma rama, solo necesitarás escribir `git push`.*

### 5. Crear el Pull Request (PR) en GitHub
1. Entra al repositorio del proyecto en **GitHub**.
2. Verás un banner amarillo que dice **"Compare & pull request"**. Haz clic ahí.
3. Describe brevemente tus cambios y etiqueta a un compañero para que revise tu código antes de unirlo a la rama principal.


## 🌿 Estructura de ramas

```
main        ← Producción. NUNCA tocar directamente.
develop     ← Rama de integración. Aquí llegan todos los Pull Requests.
walter      ← Rama personal de walter
luis        ← Rama personal de luis
angel       ← Rama personal de angel
harleth     ← Rama personal de harleth
```

---

## Instalación

```bash
# Primero crea un entorno virtual
python -m venv .venv

# Luego instala las dependencias
pip install -r backend/requirements.txt
```
