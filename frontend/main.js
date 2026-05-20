async function analyzeCode(code) {
  const response = await fetch("http://localhost:8000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Error al analizar el código");
  }

  return await response.json();
}

function renderResults(data) {
  const container = document.getElementById("results");

  const errorsHTML =
    data.errors.length > 0
      ? data.errors.map((e) => `<li>${e}</li>`).join("")
      : "<li>No se detectaron errores</li>";

  const suggestionsHTML = data.suggestions.map((s) => `<li>${s}</li>`).join("");

  container.innerHTML = `
        <div class="section">
            <h3>❌ Errores</h3>
            <ul>${errorsHTML}</ul>
        </div>
        <div class="section">
            <h3>💡 Sugerencias</h3>
            <ul>${suggestionsHTML}</ul>
        </div>
        <div class="section">
            <h3>📖 Explicación</h3>
            <p>${data.explanation}</p>
        </div>
    `;
}

document.getElementById("analyze-btn").addEventListener("click", async () => {
  const code = document.getElementById("codeInput").value;

  const btn = document.getElementById("analyze-btn");
  btn.disabled = true;
  btn.textContent = "Analizando...";

  try {
    const result = await analyzeCode(code);
    console.log("Respuesta del backend:", result); // <- añade esto
    renderResults(result);
  } catch (error) {
    document.getElementById("results").innerHTML = `
            <p class="error">Error: ${error.message}</p>
        `;
  } finally {
    btn.disabled = false;
    btn.textContent = "Analizar código";
  }
});
