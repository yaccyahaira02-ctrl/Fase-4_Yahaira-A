# Fase-4_Yahaira — Sistema Integral de Gestión de Clientes, Servicios y Reservas (Software FJ)

Proyecto desarrollado para la **Fase 4 – Prácticas simuladas** bajo el paradigma de **Programación Orientada a Objetos (POO)** en Python, sin uso de bases de datos, gestionando entidades en memoria y registrando eventos y errores en archivos de *logs*.

---


## 📁 Estructura del Proyecto

Fase-4_Yahaira/
├── excepciones.py
├── log_manager.py
├── modelos.py
├── main.py
└── README.md

---

## ¿Qué hace cada archivo?

1. **excepciones.py** define los errores propios del sistema.
2. **log_manager.py** crea la carpeta `logs` y escribe el archivo `sistema_fj.log`.
3. **modelos.py** contiene las clases de clientes, servicios y reservas. Importa las excepciones y el logger.
4. **main.py** importa las clases de `modelos.py` y ejecuta diez operaciones de prueba.