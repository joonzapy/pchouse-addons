# PC House Account

## Descripción
Este módulo introduce personalizaciones específicas para la contabilidad en PC House, incluyendo un nuevo campo `Costo Total` en las facturas de cliente. Este campo muestra el costo acumulado de los productos vendidos en la factura.

## Características
1. **Campo `Costo Total`:** 
   - Muestra el costo acumulado de los productos en las facturas.
   - Calculado a partir del costo histórico de los productos en el momento de la venta.

2. **Control de Acceso:**
   - Solo los usuarios pertenecientes al grupo "Contabilidad - Administradores" pueden ver este campo.
   - Nuevo grupo creado: **Contabilidad - Administradores**.

3. **Actualización Automática del Costo Histórico:**
   - El costo histórico de los productos se captura automáticamente:
     - Al modificar las líneas de la factura en estado borrador.
     - Al crear o confirmar una factura.

## Detalles de Implementación
### Lógica de Cálculo del Campo `Costo Total`
- El costo histórico (`historical_cost`) se almacena en las líneas de factura.
- El valor de `Costo Total` se actualiza:
  - Al modificar las líneas de factura (en modo borrador).
  - Al confirmar una factura (`action_post`).

### Cambios en Permisos y Accesos
- **Archivo:** `account_groups.xml`
  - Se define el grupo `Contabilidad - Administradores`.
- **Archivo:** `ir.model.access.csv`
  - Permisos ajustados para restringir el acceso al campo `Costo Total`.

## Instalación
1. Agregar el módulo a tu carpeta de addons.
2. Actualizar la lista de módulos: `odoo -u pchouse_account`.
3. Asegurarse de que los usuarios relevantes pertenezcan al grupo "Contabilidad - Administradores".

## Cambios Realizados
1. **Nueva funcionalidad:**
   - Campo `Costo Total` en `account.move`.
   - Campo `Costo Histórico` en `account.move.line`

2. **Seguridad:**
   - Restricción de acceso al campo `Costo Total` para el grupo "Contabilidad - Administradores".

