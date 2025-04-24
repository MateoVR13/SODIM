# SODIM - Sistema de Optimización y Distribución de Medicamentos

## Descripción
SODIM es un sistema de software diseñado para optimizar la entrega de medicamentos en EPS en Colombia. El proyecto busca reducir tiempos de espera, mejorar la trazabilidad de medicamentos y garantizar que los pacientes reciban sus tratamientos oportunamente.

## Tecnologías
- **Backend**: Django, FastAPI
- **Base de datos**: SQLite
- **Frontend**: HTML, CSS & JS

## Arquitectura

### Componentes principales
- **Backend API REST**: Gestión de órdenes, seguimiento de entregas
- **Base de datos**: Almacenamiento de información en la nube
- **Frontend**: Interfaces para pacientes, médicos, farmacias y administradores

### Flujo del sistema
1. Médico genera prescripción médica
2. Sistema verifica distribución (interna EPS o externa)
3. Gestión de inventario y disponibilidad
4. Procesamiento diferenciado (POS / No POS)
5. Confirmación y entrega de medicamentos
6. Notificación al paciente

## Beneficios

- Reducción de visitas innecesarias a farmacias
- Mejora en la planificación logística
- Prevención de desabastecimientos
- Optimización de tiempos de entrega
- Priorización basada en necesidades médicas