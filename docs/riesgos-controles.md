# Riesgos y controles verificables

Esto es un mapa de controles de la demo, no una auditoría de seguridad ni una
certificación para producción. Los nombres remiten a `tests/test_cu1.py`.

| Riesgo | Control implementado | Evidencia | Límite residual |
| --- | --- | --- | --- |
| Una evidencia da órdenes al modelo | Datos no confiables en prompt, aislamiento de E-007 y herramientas acotadas | `test_inyeccion_en_evidencia_se_aisla_y_original_se_conserva` | El detector reconoce patrones conocidos, no todas las paráfrasis de ataques |
| Mostrar datos de otra organización o rol | Identidad por conexión; filtro org en SQL; validación de rol | `test_datos_ajenos_y_rol_de_indicadores_bloqueados` y denegación en cliente MCP externo | La selección local de usuario y contraseña compartida son solo demostrativas |
| Registrar sin confirmación o reutilizar otra sesión | Firma por usuario/sesión/acción, caducidad y herramienta fuera del modelo | `test_confirmar_exige_firma_sesion_y_caducidad`, `test_agente_no_expone_herramienta_de_confirmacion` | Requiere proteger host y clave local; no es identidad productiva |
| Duplicar solicitud o superar límite concurrentemente | Transacción inmediata, revalidación e idempotencia | `test_confirmaciones_concurrentes_no_eluden_limite`, `test_confirmar_es_atomico_idempotente_y_preserva_originales` | La política adicional del cliente debe validarse con su representante |
| Alucinar fuente o dato de caso | IDs deben haber sido recibidos y caso consultado en esa pregunta | `test_agente_rechaza_citas_inventadas`, `test_agente_se_abstiene_si_no_consulto_el_caso` | Cita existente no prueba fidelidad: se necesita evaluación semántica |
| Aplicar versión derogada o esconder conflicto | Metadatos de vigencia, relación explícita del conflicto y validación de ambas citas | Pruebas de vigencia, metadatos y `test_conflicto_se_valida_aunque_la_pregunta_sea_sobre_roles` | Conflictos nuevos no se detectan automáticamente con garantías |
| Interpretar datos como SQL | Consultas del equipo, parámetros separados | `test_sql_injection_no_interpreta_argumento_como_sql` | La importación administrativa permite identificadores validados del Excel, nunca SQL del modelo |
| Alterar originales | Verificación contra Excel, triggers y estado por eventos | `test_importacion_y_originales_inmutables` | La clave y base activas no deben distribuirse como datos iniciales |
| Proveedor caído o respuesta retenida | Error explícito, sin texto alternativo inventado | `test_agente_reporta_caida_del_modelo_sin_respuesta_inventada` | Disponibilidad y variabilidad de Bonsai dependen del hardware y consulta |
| Solicitud web desde otro origen | Cookie HttpOnly/SameSite, token CSRF y filtro host/origin | `test_api_login_csrf_y_consulta_mcp` verifica sesión/CSRF; filtro host/origin revisado estáticamente | No sustituye TLS, SSO ni gestión productiva de identidades |

## Aporte del agente y verificación humana

Los commits iniciales identifican trabajo producido con el agente. En el cierre del
2026-11-01, Codex completó especificación y contratos, comparó fragmentación,
revisó semánticamente la segunda ejecución y añadió verificaciones reproducibles.
La revisión semántica se etiqueta como automatizada; no constituye validación del
cliente ni revisión humana. No se atribuye al equipo una revisión o aprobación no
registrada. El equipo debe contrastar una muestra, registrar concordancia y poder
explicar cualquier parte del código y sus límites.
