
import os
import re
#rom collections import Counter

# Filtrar entradas del /proc que son números (PIDs)
pids = [pid for pid in os.listdir("/proc") if pid.isdigit()]
#estado_resumen = Counter()

for pid in pids:
    try:
        with open(f"/proc/{pid}/status") as f:
            info = f.read()

        # Extraer campos necesarios
        name = re.search(r"^Name:\s+(.*)$", info, re.MULTILINE).group(1)
        ppid = re.search(r"^PPid:\s+(\d+)$", info, re.MULTILINE).group(1)
        estado = re.search(r"^State:\s+(\w)", info, re.MULTILINE).group(1)  # Solo la letra (R, S, Z, etc.)

        #estado_resumen[estado] += 1

        print(f"PID: {pid}")
        print(f"PPID: {ppid}")
        print(f"Nombre: {name}")
        print(f"Estado: {estado}")
        print("-" * 45)

    except Exception:
        pass  # Puede fallar si el proceso muere mientras se lee

# Mostrar resumen
# print("\nResumen de estados:")
# for estado, cantidad in estado_resumen.items():
#     print(f"{estado}: {cantidad}")
