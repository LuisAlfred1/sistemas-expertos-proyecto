from pydantic import BaseModel, Field
from typing import Literal

# Refacciones permitidas
TipoRefaccion = Literal["Chiles Rellenos", "Shucos", "Garnachas", "Ninguna"]

class SolicitudRefaccion(BaseModel):
    elaborado: bool = Field(
        ...,
        # description sirve para documentar el campo en la documentación generada por FastAPI, no afecta la validación de datos.
        description="¿Es una preparación elaborada/compleja (ej. capeado en huevo)?",
    )
    lleva_carne: bool = Field(
        ...,
        description="¿Se dispone de carne de res/cerdo (molida o picada)?",
    )
    base_pan: bool = Field(
        ...,
        description="¿Se dispone de pan de trigo como base?",
    )
    tortilla: bool = Field(
        ...,
        description="¿Se dispone de tortilla pequeña de maíz?",
    )
    ingredientes_disponibles: list[str] = Field(
        default_factory=list,
        description="Lista opcional de nombres de ingredientes específicos en inventario.",
    )


class ResultadoRefaccion(BaseModel):
    estado: Literal["exito", "ingrediente_insuficientes", "error"]
    refaccion_resultado: TipoRefaccion | None = Field(
        default=None, description="Refacción guatemalteca recomendada por el sistema."
    )
    mensaje: str = Field(
        ..., description="Mensaje informativo sobre el resultado de la recomendación."
    )
    justificacion: str | None = Field(
        default=None,
        description="Justificación de la recomendación basada en los criterios de selección.",
    )
    regla: str | None = Field(
        default=None,
        description="Identificador de la regla disparada ((ej. R01-Ofrecer-Chiles-Rellenos).)",
    )
