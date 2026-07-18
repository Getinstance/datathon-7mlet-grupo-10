const API_BASE = 'http://localhost:8000';
const profileSelect = document.getElementById('profileSelect');
const recommendButton = document.getElementById('recommendButton');
const result = document.getElementById('result');

async function loadProfiles() {
  const response = await fetch(`${API_BASE}/profiles`);
  if (!response.ok) {
    throw new Error('Não foi possível carregar os perfis');
  }
  const profiles = await response.json();
  profileSelect.innerHTML = profiles
    .map((profile) => `<option value="${profile.id}">${profile.name} · ${profile.context}</option>`)
    .join('');
}

async function recommendOffer() {
  result.innerHTML = '<p class="muted">Consultando o modelo...</p>';
  const response = await fetch(`${API_BASE}/recommendation`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ profile_id: profileSelect.value }),
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.detail || 'Erro ao consultar recomendação');
  }

  const rankedList = payload.ranked_offers
    .map((item) => `<li><strong>${item.offer}</strong> · score ${item.score}</li>`)
    .join('');

  result.innerHTML = `
    <div class="offer-banner">Oferta recomendada: <span>${payload.recommended_offer}</span></div>
    <p><strong>Cliente:</strong> ${payload.profile.name}</p>
    <p class="muted">${payload.profile.description}</p>
    <p><strong>Contexto:</strong> <code>${payload.context}</code></p>
    <ul>${rankedList}</ul>
  `;
}

recommendButton.addEventListener('click', recommendOffer);

(async () => {
  try {
    await loadProfiles();
    await recommendOffer();
  } catch (error) {
    result.innerHTML = `<p class="muted">${error.message}</p>`;
  }
})();
