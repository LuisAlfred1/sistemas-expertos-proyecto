// Vista de recomendaciones (JavaScript vanilla)
// Se conecta con el backend FastAPI:  GET /api/opciones  y  POST /api/recomendar

const API = "http://localhost:8000/api"; // cámbialo cuando despliegues

// Etiquetas bonitas (el motor usa símbolos sin tildes ni espacios)
const ETIQUETAS = {
  antojito: "Antojito",
  postre: "Postre",
  plato_fuerte: "Plato fuerte",
  platano: "Plátano",
  ajonjoli: "Ajonjolí",
  azucar: "Azúcar",
  aguacate: "Aguacate (guacamol)",
};
const etiqueta = (s) =>
  ETIQUETAS[s] ?? s.charAt(0).toUpperCase() + s.slice(1).replaceAll("_", " ");

const NIVELES = {
  exacta: "Coincidencia exacta",
  categoria: "Por categoría",
  ingrediente: "Por ingrediente",
  alternativa: "Opción alternativa",
};

const form = document.getElementById("rform");
const selCategoria = document.getElementById("selCategoria");
const selIngrediente = document.getElementById("selIngrediente");
const btn = document.getElementById("btnRecomendar");
const mensaje = document.getElementById("mensaje");
const zona = document.getElementById("zonaResultados");
const resultado = document.getElementById("resultado");

function llenarSelect(select, valores, textoPorDefecto) {
  select.replaceChildren(new Option(textoPorDefecto, "cualquiera"));
  valores.forEach((v) => select.add(new Option(etiqueta(v), v)));
}

function mostrarMensaje(texto, esError = false) {
  mensaje.textContent = texto;
  mensaje.classList.toggle("is-error", esError);
  zona.hidden = !texto && resultado.children.length === 0;
}

async function cargarOpciones() {
  try {
    const res = await fetch(`${API}/opciones`);
    if (!res.ok) throw new Error();
    const data = await res.json();
    llenarSelect(selCategoria, data.categorias, "Cualquier categoría");
    llenarSelect(selIngrediente, data.ingredientes, "Cualquier ingrediente");
  } catch {
    mostrarMensaje("No se pudieron cargar las opciones. Intenta más tarde.", true);
  }
}

// Cada recomendación es un <li> con la misma estructura que .menu-list del tema
function crearItem(r) {
  const li = document.createElement("li");
  li.className = "menu-list__item";

  const desc = document.createElement("div");
  desc.className = "menu-list__item-desc";

  const titulo = document.createElement("h4");
  titulo.textContent = r.platillo;

  const meta = document.createElement("p");
  meta.className = "reco-meta";
  meta.textContent = `${etiqueta(r.categoria)} · ${r.sabor} · ${r.porciones} porciones`;

  const texto = document.createElement("p");
  texto.textContent = r.descripcion ?? "";

  const porque = document.createElement("p");
  porque.className = "reco-porque";
  porque.textContent = r.justificacion ?? "";

  desc.append(titulo, meta, texto, porque);

  const nivel = document.createElement("div");
  nivel.className = "reco-nivel" + (r.nivel === "alternativa" ? " reco-nivel--alternativa" : "");
  nivel.textContent = NIVELES[r.nivel] ?? "";

  li.append(desc, nivel);
  return li;
}

async function recomendar(evento) {
  evento.preventDefault(); // evita que el formulario recargue la página

  resultado.replaceChildren();
  const cuerpo = { categoria: selCategoria.value, ingrediente: selIngrediente.value };

  if (cuerpo.categoria === "cualquiera" && cuerpo.ingrediente === "cualquiera") {
    mostrarMensaje("Elige al menos una categoría o un ingrediente.", true);
    return;
  }

  btn.disabled = true;
  const textoOriginal = btn.textContent;
  btn.textContent = "Buscando...";

  try {
    const res = await fetch(`${API}/recomendar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(cuerpo),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      mostrarMensaje(typeof err.detail === "string" ? err.detail : "Ocurrió un error.", true);
      return;
    }

    const data = await res.json();

    if (data.estado === "exito" || data.estado === "alternativas") {
      data.recomendaciones.forEach((r) => resultado.append(crearItem(r)));
      mostrarMensaje(data.mensaje);
      zona.hidden = false;
      zona.scrollIntoView({ behavior: "smooth", block: "start" });
    } else {
      mostrarMensaje(data.mensaje || "No encontramos un platillo con esas características.", true);
    }
  } catch {
    mostrarMensaje("No se pudo conectar con el servidor.", true);
  } finally {
    btn.disabled = false;
    btn.textContent = textoOriginal;
  }
}

form.addEventListener("submit", recomendar);
cargarOpciones();
