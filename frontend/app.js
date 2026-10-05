const API_BASE_URL = "/api/v1";

const form = document.querySelector("#evaluation-form");
const apiStatus = document.querySelector("#api-status");
const resultSection = document.querySelector("#result");

async function checkApiHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error(`La API respondió con HTTP ${response.status}.`);
    }

    const health = await response.json();
    apiStatus.textContent = `API conectada: ${health.sistema} (${health.motor}).`;
    apiStatus.classList.add("is-connected");
  } catch (error) {
    apiStatus.textContent = `No se pudo conectar con la API. ${error.message}`;
    apiStatus.classList.add("is-error");
  }
}

function showResult(title, details, isError = false) {
  resultSection.replaceChildren();
  resultSection.hidden = false;
  resultSection.classList.toggle("is-error", isError);

  const heading = document.createElement("h2");
  heading.textContent = title;
  resultSection.append(heading);

  for (const detail of details) {
    if (!detail.value) continue;

    const paragraph = document.createElement("p");
    const label = document.createElement("strong");
    label.textContent = `${detail.label}: `;
    paragraph.append(label, document.createTextNode(detail.value));
    resultSection.append(paragraph);
  }
}

function getApiErrorMessage(body, status) {
  if (typeof body.detail === "string") return body.detail;

  if (Array.isArray(body.detail)) {
    return body.detail
      .map((error) => error.msg)
      .filter(Boolean)
      .join(" ");
  }

  return body.mensaje || `La solicitud falló con HTTP ${status}.`;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const submitButton = form.querySelector('button[type="submit"]');
  submitButton.disabled = true;
  submitButton.textContent = "Consultando...";
  resultSection.hidden = true;

  const formData = new FormData(form);
  const requestBody = {
    elaborado: formData.get("elaborado") === "true",
    lleva_carne: formData.get("lleva_carne") === "true",
    base_pan: formData.get("base_pan") === "true",
    tortilla: formData.get("tortilla") === "true",
    ingredientes_disponibles: formData
      .get("ingredientes_disponibles")
      .split(",")
      .map((ingredient) => ingredient.trim())
      .filter(Boolean),
  };

  try {
    const response = await fetch(`${API_BASE_URL}/evaluar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });
    const body = await response.json();

    if (!response.ok) {
      throw new Error(getApiErrorMessage(body, response.status));
    }

    showResult(
      body.refaccion_resultado || body.mensaje,
      [
        { label: "Estado", value: body.estado },
        { label: "Mensaje", value: body.mensaje },
        { label: "Justificación", value: body.justificacion },
        { label: "Regla aplicada", value: body.regla },
      ],
      body.estado === "error",
    );
  } catch (error) {
    showResult("No se pudo obtener la recomendación", [{ label: "Error", value: error.message }], true);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Consultar recomendación";
  }
});

checkApiHealth();