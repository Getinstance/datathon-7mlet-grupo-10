from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

APP_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = APP_ROOT.parents[0]
MODEL_PATH = REPO_ROOT / "data" / "model" / "thompson_sampling_contextual_model.json"

app = FastAPI(title="FIAP BANK Demo API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecommendationRequest(BaseModel):
    profile_id: str


class Profile(BaseModel):
    id: str
    name: str
    context: str
    description: str


def load_model() -> dict[str, Any]:
    with MODEL_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


MODEL = load_model()
PROFILES = [
    Profile(
        id="ana-martins",
        name="Ana Martins",
        context="Canal_App Push_Cluster_4_Emprestimo_0_age_Adulto",
        description="Cliente adulta, canal app push, perfil de investimento conservador.",
    ),
    Profile(
        id="bruno-costa",
        name="Bruno Costa",
        context="Canal_SMS_Cluster_3_Emprestimo_0_age_Adulto",
        description="Cliente adulto, alto interesse em serviços e comunicação por SMS.",
    ),
    Profile(
        id="camila-souza",
        name="Camila Souza",
        context="Canal_Banner_Cluster_2_Emprestimo_0_age_Senior",
        description="Cliente senior, canal banner, perfil com baixo histórico de crédito.",
    ),
    Profile(
        id="daniel-rocha",
        name="Daniel Rocha",
        context="Canal_Email_Cluster_4_Emprestimo_0_age_Adulto",
        description="Cliente adulto, canal e-mail, perfil com boa abertura a crédito.",
    ),
    Profile(
        id="elisa-nogueira",
        name="Elisa Nogueira",
        context="Canal_App Push_Cluster_1_Emprestimo_0_age_Jovem",
        description="Cliente jovem, canal app push, forte interesse em seguros.",
    ),
    Profile(
        id="felipe-lima",
        name="Felipe Lima",
        context="Canal_Banner_Cluster_5_Emprestimo_0_age_Jovem",
        description="Cliente jovem, canal banner, comportamento de serviços e investimento.",
    ),
    Profile(
        id="giovana-reis",
        name="Giovana Reis",
        context="Canal_Email_Cluster_3_Emprestimo_2_age_Adulto",
        description="Cliente adulta, canal e-mail, perfil com relacionamento mais antigo.",
    ),
    Profile(
        id="henrique-torres",
        name="Henrique Torres",
        context="Canal_SMS_Cluster_1_Emprestimo_2_age_Jovem",
        description="Cliente jovem, canal SMS, perfil com maior probabilidade de crédito.",
    ),
    Profile(
        id="isabela-mendes",
        name="Isabela Mendes",
        context="Canal_App Push_Cluster_2_Emprestimo_0_age_Adulto",
        description="Cliente adulta, canal app push, forte tendência a investimento.",
    ),
    Profile(
        id="joao-pereira",
        name="João Pereira",
        context="Canal_Banner_Cluster_0_Emprestimo_2_age_Adulto",
        description="Cliente adulto, canal banner, foco em produtos de empréstimo e crédito.",
    ),
    Profile(
        id="larissa-almeida",
        name="Larissa Almeida",
        context="Canal_Email_Cluster_0_Emprestimo_0_age_Jovem",
        description="Cliente jovem, canal e-mail, perfil com interesse equilibrado.",
    ),
    Profile(
        id="miguel-santos",
        name="Miguel Santos",
        context="Canal_SMS_Cluster_5_Emprestimo_2_age_Adulto",
        description="Cliente adulto, canal SMS, perfil com alta preferência por seguros.",
    ),
]


def recommend_offer(context: str) -> dict[str, Any]:
    if context not in MODEL:
        raise HTTPException(status_code=404, detail=f"Contexto não encontrado: {context}")

    context_model = MODEL[context]
    alphas = context_model["alphas"]
    betas = context_model["betas"]

    digest = hashlib.sha256(context.encode("utf-8")).hexdigest()
    seed = int(digest[:8], 16)
    rng = np.random.default_rng(seed)

    scores: list[tuple[float, str]] = []
    for offer_name in alphas:
        sample = float(rng.beta(alphas[offer_name], betas[offer_name]))
        scores.append((sample, offer_name))

    best_offer = max(scores, key=lambda item: item[0])[1]
    ranked = [
        {"offer": offer_name, "score": round(score, 4)}
        for score, offer_name in sorted(scores, key=lambda item: item[0], reverse=True)
    ]

    return {
        "context": context,
        "recommended_offer": best_offer,
        "ranked_offers": ranked,
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/profiles", response_model=list[Profile])
def list_profiles() -> list[Profile]:
    return PROFILES


@app.post("/recommendation")
def create_recommendation(request: RecommendationRequest) -> dict[str, Any]:
    profile = next((item for item in PROFILES if item.id == request.profile_id), None)
    if profile is None:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")

    result = recommend_offer(profile.context)
    result["profile"] = {"id": profile.id, "name": profile.name, "description": profile.description}
    return result
