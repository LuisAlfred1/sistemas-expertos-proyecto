from typing import Literal

from pydantic import BaseModel, Field


class SolicitudRecomendacion(BaseModel):
    """Lo que envía el frontend: categoría e/o ingrediente ("cualquiera" = no filtra)."""

    categoria: str = Field(
        default="cualquiera",
        # description solo documenta el campo en Swagger (/docs), no afecta la validación.
        description="Categoría deseada: antojito, postre, plato_fuerte o cualquiera.",
    )
    ingrediente: str = Field(
        default="cualquiera",
        description="Ingrediente deseado (ej. pollo, platano, tortilla) o cualquiera.",
    )


class Recomendacion(BaseModel):
    """Un platillo recomendado por el motor."""

    platillo: str
    nivel: Literal["exacta", "categoria", "ingrediente", "alternativa", "ninguna"]
    puntaje: int = Field(
        ..., description="100 coincidencia exacta, 80 un filtro, 50 alternativa."
    )
    mensaje: str
    justificacion: str | None = None
    regla: str | None = Field(
        default=None,
        description="Regla disparada (ej. R01-Coincidencia-Exacta).",
    )
    categoria: str | None = None
    sabor: str | None = None
    descripcion: str | None = None
    porciones: str | None = None
    pagina: int | None = Field(default=None, description="Página del compendio PDF.")


class ResultadoRecomendacion(BaseModel):
    estado: Literal["exito", "alternativas", "sin_resultado", "error"]
    mensaje: str
    recomendaciones: list[Recomendacion] = Field(default_factory=list)


class OpcionesDisponibles(BaseModel):
    categorias: list[str]
    ingredientes: list[str]
