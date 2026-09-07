; SISTEMA EXPERTO DE SELECCION DE REFACCIONES

(deftemplate preparacion
   (slot elaborado)       ; "si" o "no"
   (slot lleva_carne)     ; "si" o "no"
   (slot base_pan)        ; "si" o "no"
   (slot tortilla)        ; "si" o "no"
)

(deftemplate resultado
   (slot preparacion)
   (slot mensaje)
   (slot justificacion)
   (slot regla)
)

; REGLAS DEL SISTEMA EXPERTO

; --- REGLA R01: OFRECER CHILES RELLENOS ---

(defrule ofrecer-chiles-rellenos
   (declare (salience 100))
   (preparacion (elaborado "si") (lleva_carne "si"))
   (not (resultado))
   =>
   (assert (resultado
      (preparacion "Chiles Rellenos")
      (mensaje "Ofrecer chiles rellenos")
      (justificacion "Requiere una preparación culinaria elaborada (capeado con huevo) y obligatoriamente lleva carne picada como relleno.")
      (regla "R01-Ofrecer-Chiles-Rellenos")
   ))
)

; --- REGLA R02: INGREDIENTES INSUFICIENTES (RAMA ELABORADOS) ---

(defrule insuficientes-elaborados
   (declare (salience 100))
   (preparacion (elaborado "si") (lleva_carne "no"))
   (not (resultado))
   =>
   (assert (resultado
      (preparacion "Ninguna")
      (mensaje "Ingredientes insuficientes")
      (justificacion "Aunque requiere una preparación, no se dispone de carne para rellenar los chiles.")
      (regla "R02-Insuficientes-Elaborados")
   ))
)

; --- REGLA R03: OFRECER SHUCOS ---

(defrule ofrecer-shucos
   (declare (salience 100))
   (preparacion (elaborado "no") (base_pan "si"))
   (not (resultado))
   =>
   (assert (resultado
      (preparacion "Shucos")
      (mensaje "Ofrecer shucos")
      (justificacion "La refacción utiliza pan de trigo como base para los embutidos.")
      (regla "R03-Ofrecer-Shucos")
   ))
)

; --- REGLA R04: OFRECER GARNACHAS ---

(defrule ofrecer-garnachas
   (declare (salience 100))
   (preparacion (elaborado "no") (base_pan "no") (tortilla "si"))
   (not (resultado))
   =>
   (assert (resultado
      (preparacion "Garnachas")
      (mensaje "Ofrecer garnacha")
      (justificacion "La refacción no utiliza pan y se monta sobre tortilla de maíz pequeña.")
      (regla "R04-Ofrecer-Garnachas")
   ))
)

; --- REGLA R05: INGREDIENTES INSUFICIENTES (RAMA NO ELABORADOS) ---

(defrule insuficientes-no-elaborados
   (declare (salience 100))
   (preparacion (elaborado "no") (base_pan "no") (tortilla "no"))
   (not (resultado))
   =>
   (assert (resultado
      (preparacion "Ninguna")
      (mensaje "Ingredientes insuficientes")
      (justificacion "No se dispone de ninguna base (ni pan de trigo ni tortilla de maíz) para armar la refacción.")
      (regla "R05-Insuficientes-No-Elaborados")
   ))
)