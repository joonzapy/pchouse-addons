===============================
PCHouse Sale
===============================

Este módulo personalizado extiende la funcionalidad del módulo de Ventas de Odoo al introducir reglas dinámicas de precios basadas en grupos de usuarios y desbloqueando el campo de precio unitario en las líneas de pedido de venta con validaciones adicionales.

Características principales
---------------------------

1. **Tarifas dinámicas basadas en grupos de usuarios**:
   - Se agregó el campo `user_groups` al modelo de Tarifas (`product.pricelist`), permitiendo asociar tarifas con grupos específicos de usuarios.
   - Al crear un pedido de venta, el sistema determina automáticamente la tarifa aplicable en función del grupo al que pertenece el usuario actual.

2. **Validación de precio mínimo**:
   - Garantiza que el precio unitario (`price_unit`) ingresado en las líneas del pedido de venta no sea inferior al precio mínimo definido por la tarifa asociada.
   - Muestra un error de validación si el precio ingresado está por debajo del precio mínimo.

3. **Desbloqueo del campo de precio unitario**:
   - El campo de precio unitario en las líneas del pedido de venta ahora es editable para los usuarios que pertenecen a grupos específicos.
   - Incluye validaciones adicionales para evitar errores al realizar ajustes manuales.

Configuración
-------------

### Tarifas
1. Navega a **Ventas > Configuración > Tarifas**.
2. Abre o crea una tarifa.
3. Utiliza el nuevo campo **Grupos de Usuarios** para especificar los grupos de usuarios que pueden utilizar esta tarifa.

### Pedidos de Venta
- Cuando se agrega un producto a una línea del pedido de venta, el sistema realiza las siguientes acciones:
  1. Identifica la tarifa activa en función del grupo del usuario.
  2. Calcula el precio mínimo del producto utilizando las reglas de la tarifa.
  3. Permite a los usuarios editar el precio unitario, pero aplica la validación del precio mínimo.