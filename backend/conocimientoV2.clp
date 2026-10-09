; ============================================================
; SISTEMA EXPERTO DE RECOMENDACION DE COMIDA GUATEMALTECA
; Fuente: Compendio de Recetas, Tecnicas Ancestrales y Modernas
;         de la Gastronomia Guatemalteca (Universidad Galileo, 2017)
; ============================================================

; ---------- PLANTILLAS ----------

; Hecho de conocimiento: un platillo del documento
(deftemplate platillo
   (slot nombre)
   (slot categoria)            ; antojito | postre | plato_fuerte
   (slot sabor)                ; salado | dulce
   (multislot ingredientes)    ; simbolos sin tildes ni espacios
   (slot descripcion)
   (slot porciones)
   (slot pagina))              ; pagina del PDF

; Hecho de entrada: lo que elige el usuario ("cualquiera" = no filtra)
(deftemplate solicitud
   (slot categoria   (default cualquiera))
   (slot ingrediente (default cualquiera)))

; Hecho de salida: una recomendacion (puede haber varias)
(deftemplate recomendacion
   (slot platillo)
   (slot nivel)                ; exacta | categoria | ingrediente | alternativa | ninguna
   (slot puntaje (type INTEGER))
   (slot mensaje)
   (slot justificacion)
   (slot regla))

; ---------- BASE DE HECHOS (platillos del PDF) ----------

(deffacts base-de-platillos

   (platillo
      (nombre "Tostadas de guacamol")
      (categoria antojito) (sabor salado)
      (ingredientes tortilla aguacate queso cebolla perejil)
      (descripcion "Tortillas fritas cubiertas con guacamol, queso seco, perejil y cebolla en rodajas.")
      (porciones "4-6") (pagina 124))

   (platillo
      (nombre "Garnachas")
      (categoria antojito) (sabor salado)
      (ingredientes tortilla carne lechuga tomate mayonesa queso cebolla)
      (descripcion "Tortillas de maiz fritas con carne molida, lechuga con limon, salsa de tomate y queso.")
      (porciones "4-6") (pagina 135))

   (platillo
      (nombre "Shucos")
      (categoria antojito) (sabor salado)
      (ingredientes pan salchicha aguacate repollo cebolla cilantro mayonesa)
      (descripcion "Pan relleno de embutidos asados con guacamol, repollo, cebolla y aderezos.")
      (porciones "8-12") (pagina 134))

   (platillo
      (nombre "Pollo guisado")
      (categoria plato_fuerte) (sabor salado)
      (ingredientes pollo papa tomate cebolla ajo)
      (descripcion "Pollo con papas en salsa de tomate y miltomate; se sirve con arroz.")
      (porciones "6") (pagina 123))

   (platillo
      (nombre "Platanos en mole")
      (categoria postre) (sabor dulce)
      (ingredientes platano chocolate pepitoria ajonjoli canela tomate chile pan)
      (descripcion "Platanos maduros fritos banados en una salsa de chocolate, semillas y especias. Postre de San Marcos.")
      (porciones "8") (pagina 159))

   (platillo
      (nombre "Rellenitos de platano")
      (categoria postre) (sabor dulce)
      (ingredientes platano frijol azucar canela)
      (descripcion "Masa de platano maduro rellenas de frijol dulce, fritas y espolvoreadas con azucar.")
      (porciones "8") (pagina 158))
)

; ---------- REGLAS ----------

; R01: categoria E ingrediente coinciden en el mismo platillo
(defrule r01-coincidencia-exacta
   (declare (salience 100))
   (solicitud (categoria ?c&~cualquiera) (ingrediente ?i&~cualquiera))
   (platillo (nombre ?n) (categoria ?c) (ingredientes $? ?i $?) (pagina ?p))
   =>
   (assert (recomendacion
      (platillo ?n)
      (nivel exacta)
      (puntaje 100)
      (mensaje "Coincide con lo que pediste")
      (justificacion (str-cat "Es de la categoria " ?c " y lleva " ?i " (receta en la pagina " ?p " del compendio)."))
      (regla "R01-Coincidencia-Exacta"))))

; R02: el usuario solo eligio categoria
(defrule r02-solo-categoria
   (declare (salience 90))
   (solicitud (categoria ?c&~cualquiera) (ingrediente cualquiera))
   (platillo (nombre ?n) (categoria ?c) (pagina ?p))
   =>
   (assert (recomendacion
      (platillo ?n)
      (nivel categoria)
      (puntaje 80)
      (mensaje "Platillo de la categoria elegida")
      (justificacion (str-cat "Pertenece a la categoria " ?c " (pagina " ?p " del compendio)."))
      (regla "R02-Solo-Categoria"))))

; R03: el usuario solo eligio ingrediente
(defrule r03-solo-ingrediente
   (declare (salience 90))
   (solicitud (categoria cualquiera) (ingrediente ?i&~cualquiera))
   (platillo (nombre ?n) (ingredientes $? ?i $?) (pagina ?p))
   =>
   (assert (recomendacion
      (platillo ?n)
      (nivel ingrediente)
      (puntaje 80)
      (mensaje "Platillo que lleva ese ingrediente")
      (justificacion (str-cat "Entre sus ingredientes esta " ?i " (pagina " ?p " del compendio)."))
      (regla "R03-Solo-Ingrediente"))))

; R04: eligio ambos, no hubo coincidencia exacta -> alternativas por categoria
(defrule r04-alternativa-por-categoria
   (declare (salience 50))
   (solicitud (categoria ?c&~cualquiera) (ingrediente ?i&~cualquiera))
   (not (recomendacion (nivel exacta)))
   (platillo (nombre ?n) (categoria ?c) (pagina ?p))
   =>
   (assert (recomendacion
      (platillo ?n)
      (nivel alternativa)
      (puntaje 50)
      (mensaje (str-cat "No hay platillo de esa categoria con " ?i ", pero esta es una opcion de la categoria"))
      (justificacion (str-cat "Pertenece a la categoria " ?c " (pagina " ?p " del compendio)."))
      (regla "R04-Alternativa-Por-Categoria"))))

; R05: eligio ambos, no hubo coincidencia exacta -> alternativas por ingrediente
(defrule r05-alternativa-por-ingrediente
   (declare (salience 50))
   (solicitud (categoria ?c&~cualquiera) (ingrediente ?i&~cualquiera))
   (not (recomendacion (nivel exacta)))
   (platillo (nombre ?n) (ingredientes $? ?i $?) (pagina ?p))
   =>
   (assert (recomendacion
      (platillo ?n)
      (nivel alternativa)
      (puntaje 50)
      (mensaje (str-cat "No hay platillo de la categoria " ?c " con ese ingrediente, pero este lleva " ?i))
      (justificacion (str-cat "Entre sus ingredientes esta " ?i " (pagina " ?p " del compendio)."))
      (regla "R05-Alternativa-Por-Ingrediente"))))

; R06: ninguna regla produjo recomendacion
(defrule r06-sin-resultado
   (declare (salience -10))
   (solicitud)
   (not (recomendacion))
   =>
   (assert (recomendacion
      (platillo "Ninguno")
      (nivel ninguna)
      (puntaje 0)
      (mensaje "Sin recomendacion")
      (justificacion "Ningun platillo de la base de conocimiento cumple con lo solicitado.")
      (regla "R06-Sin-Resultado"))))
