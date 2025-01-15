# pchouse_stock

**Gestión Personalizada de Inventario**

Este módulo proporciona una gestión personalizada del inventario para satisfacer las necesidades específicas de la empresa.

---

## Características

1. **Nuevo grupo de usuarios:**
   - Se crea un grupo llamado **Gestión de Inventario** para manejar operaciones relacionadas con el inventario.

2. **Modificación de permisos del botón "Devolver":**
   - Los usuarios del grupo **Gestión de Inventario** ahora pueden acceder al botón "Devolver" en las transferencias de stock (`stock.picking`).
   - Los permisos del grupo **Administradores de Inventario** se mantienen intactos.
   - Los permisos actuales de otros grupos no se ven afectados.

3. **Seguridad y control:**
   - Se asegura que las modificaciones no interfieran con otras funcionalidades del modelo `stock.picking`.

