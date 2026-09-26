from pathlib import Path
import clips


archivo_clp = Path(__file__).parent.parent / "backend" / "conocimiento.clp"

#prueba R1
env = clips.Environment()

env.load(str(archivo_clp))

env.assert_string("""(
    preparacion 
    (elaborado "si") 
    (lleva_carne "si") 
    (base_pan "no") 
    (tortilla "no")
    )""")

print("\n=== Agenda Inicial ===")
print(env.eval("(agenda)"))

env.eval("(watch rules)")

print("\n=== Ejecutando Prueba 01 ===")
env.run()

print("\n=== Hechos Finales ===")
for fact in env.facts():
    print(fact)


#prueba R2
env = clips.Environment()

env.load(str(archivo_clp))

env.assert_string("""(
    preparacion 
    (elaborado "si") 
    (lleva_carne "no") 
    (base_pan "no") 
    (tortilla "no")
    )""")

print("\n=== Agenda Inicial ===")
print(env.eval("(agenda)"))

env.eval("(watch rules)")

print("\n=== Ejecutando Prueba 02 ===")
env.run()

print("\n=== Hechos Finales ===")
for fact in env.facts():
    print(fact)


#prueba R3
env = clips.Environment()

env.load(str(archivo_clp))

env.assert_string("""(
    preparacion 
    (elaborado "no") 
    (lleva_carne"si") 
    (base_pan "si") 
    (tortilla "no")
    )""")


print("\n=== Agenda Inicial ===")
print(env.eval("(agenda)"))

env.eval("(watch rules)")

print("\n=== Ejecutando Prueba 03 ===")
env.run()

print("\n=== Hechos Finales ===")
for fact in env.facts():
    print(fact)


#prueba R4
env = clips.Environment()

env.load(str(archivo_clp))

env.assert_string("""(
    preparacion 
    (elaborado "no") 
    (lleva_carne "no") 
    (base_pan "no") 
    (tortilla "si")
    )""")


print("\n=== Agenda Inicial ===")
print(env.eval("(agenda)"))

env.eval("(watch rules)")

print("\n=== Ejecutando Prueba 04 ===")
env.run()

print("\n=== Hechos Finales ===")
for fact in env.facts():
    print(fact)

#prueba R5
env = clips.Environment()

env.load(str(archivo_clp))

env.assert_string("""(
    preparacion 
    (elaborado "no") 
    (lleva_carne "no") 
    (base_pan "no") 
    (tortilla "no")
    )""")


print("\n=== Agenda Inicial ===")
print(env.eval("(agenda)"))

env.eval("(watch rules)")

print("\n=== Ejecutando Prueba 05 ===")
env.run()

print("\n=== Hechos Finales ===")
for fact in env.facts():
    print(fact)
