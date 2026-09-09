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
2. Verás un banner verde que dice **"Compare & pull request"**. Haz clic ahí.
3. Selecciona la rama **develop**, escribe brevemente tus cambios y crea el PR.


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
pip install -r backend/requeriments.txt
```

---

## Proceso para unir los últimos cambios de la rama main

Sigue estos pasos en tu terminal para integrar los cambios más recientes de **main** en tu rama actual de trabajo de forma segura.

## 1. Asegurar tus cambios locales
Antes de moverte entre ramas o fusionar código, debes asegurarte de que tu espacio de trabajo esté limpio.
* **Opción A (Recomendada):** Si tus cambios están listos, hazles commit:
  ```bash
  git add .
  git commit -m "Guarda tus cambios actuales"
  ```
* **Opción B:** Si tus cambios están incompletos y no quieres hacer un commit todavía, guárdalos temporalmente:
  ```bash
  git stash
  ```

## 2. Descargar las últimas actualizaciones
Trae la información más reciente desde el repositorio remoto (GitHub, GitLab, etc.) sin modificar tu código local todavía:
```bash
git fetch origin
```

## 3. Asegurar tu posición en tu rama de trabajo
Confirma que te encuentras en tu rama personal para recibir los cambios de `main`:
```bash
git checkout <tu-rama>
```

## 4. Fusionar los cambios de main
Une los cambios actualizados de la rama principal dentro de tu rama local:
```bash
git merge origin/main
```

> 💡 **Nota sobre conflictos:** Si Git encuentra modificaciones en las mismas líneas de código que tú tocaste, detendrá el proceso y te pedirá resolver los conflictos. Una vez resueltos en tu editor de código, ejecuta `git add .` y `git commit` para finalizar la fusión.

## 5. Recuperar tus cambios guardados (Opcional)
Si en el paso 1 decidiste guardar tus cambios con `git stash`, ahora puedes traerlos de vuelta para seguir trabajando:
```bash
git stash pop
```

