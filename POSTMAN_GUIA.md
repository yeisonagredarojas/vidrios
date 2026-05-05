# 🧪 Guía completa de pruebas en Postman

Base URL: http://localhost:8000

---

## 1. AUTENTICACIÓN (JWT)

### Obtener token
POST /api/auth/token/
Body (JSON):
{
  "username": "admin",
  "password": "admin123"
}
→ Respuesta: { "access": "eyJ...", "refresh": "eyJ..." }

### Usar el token
En todas las peticiones siguientes agrega el header:
Authorization: Bearer eyJ...  (el access token)

### Renovar token
POST /api/auth/token/refresh/
Body: { "refresh": "eyJ..." }

---

## 2. COTIZACIÓN (NO requiere token)

POST /api/cotizaciones/calcular/
Body:
{
  "tipo_vidrio": "normal",
  "ancho": 1.5,
  "alto": 2.0,
  "tipo_trabajo": "instalacion",
  "es_envio_nacional": false
}

Tipos de vidrio: normal | tallado | espejo | templado | laminado
Tipos de trabajo: corte | instalacion | diseno | corte_instalacion

---

## 3. CLIENTES

GET    /api/clientes/              → listar todos
GET    /api/clientes/?search=maria → buscar por nombre/teléfono
GET    /api/clientes/?ciudad=Tumaco → filtrar por ciudad
GET    /api/clientes/1/            → detalle de cliente (incluye deuda)
POST   /api/clientes/              → crear cliente
PATCH  /api/clientes/1/            → editar parcial
DELETE /api/clientes/1/            → eliminar

Body para crear/editar:
{
  "nombre": "Juan Perez",
  "telefono": "3001234567",
  "correo": "juan@email.com",
  "ciudad": "Tumaco",
  "direccion": "Calle 10 # 5-20"
}

---

## 4. PEDIDOS

GET    /api/pedidos/               → listar todos
GET    /api/pedidos/?estado=cotizado       → filtrar por estado
GET    /api/pedidos/?tipo_vidrio=espejo    → filtrar por tipo
GET    /api/pedidos/?cliente=1            → pedidos de un cliente
GET    /api/pedidos/1/             → detalle con saldo pendiente
POST   /api/pedidos/               → crear (precio se calcula solo)
PATCH  /api/pedidos/1/             → editar (cambiar estado, asignar trabajador)

Body para crear:
{
  "cliente": 1,
  "tipo_vidrio": "normal",
  "ancho": "1.500",
  "alto": "2.000",
  "tipo_trabajo": "corte",
  "ciudad_entrega": "Tumaco",
  "es_envio_nacional": false,
  "descripcion": "Ventana sala"
}
→ El campo precio_total se calcula automaticamente

Body para cambiar estado:
PATCH /api/pedidos/1/
{ "estado": "en_proceso" }

Estados: cotizado → abonado → en_proceso → terminado | cancelado

---

## 5. PAGOS

GET    /api/pagos/                 → historial de pagos
GET    /api/pagos/deudas/          → clientes con saldo pendiente
POST   /api/pagos/                 → registrar pago (actualiza estado del pedido)

Body para registrar pago:
{
  "cliente": 1,
  "pedido": 1,
  "monto": "50000",
  "fecha_pago": "2025-04-20",
  "tipo_pago": "nequi",
  "referencia": "TRX123456"
}

Tipos de pago: efectivo | transferencia | nequi | daviplata | otro

---

## 6. INVENTARIO

GET    /api/inventario/            → listar materiales
GET    /api/inventario/bajo-stock/ → solo los que tienen stock critico
POST   /api/inventario/            → agregar material
PATCH  /api/inventario/1/          → actualizar cantidad/precio

Body:
{
  "tipo_material": "Vidrio Normal 4mm",
  "cantidad": "50.000",
  "unidad": "m2",
  "stock_minimo": "10.000",
  "precio_compra": "18000"
}

Unidades: m2 | unidad | kg | litros | metros

---

## 7. TRABAJADORES

GET    /api/trabajadores/          → listar
POST   /api/trabajadores/          → crear
PATCH  /api/trabajadores/1/        → editar

Body:
{
  "nombre": "Pedro Gomez",
  "rol": "cortador",
  "telefono": "3009876543"
}

Roles: cortador | instalador | disenador | vendedor | administrador | conductor

---

## 8. PROVEEDORES

GET    /api/proveedores/           → listar
POST   /api/proveedores/           → crear
PATCH  /api/proveedores/1/         → editar

Body:
{
  "nombre": "Vidriera Central S.A.",
  "contacto": "Carlos Lopez",
  "telefono": "3111234567",
  "ciudad": "Pasto",
  "tipo_material": "Vidrio float y templado"
}

---

## 9. CONFIGURACIÓN DE PRECIOS

GET   /api/cotizaciones/config/    → ver precios actuales
PATCH /api/cotizaciones/config/1/  → modificar precios

Body (solo los campos que quieras cambiar):
{
  "precio_vidrio_normal_m2": "28000",
  "costo_transporte_local": "20000"
}

---

## FLUJO COMPLETO DE UN PEDIDO

1. POST /api/auth/token/           → obtener token
2. POST /api/clientes/             → crear cliente
3. POST /api/cotizaciones/calcular/ → ver precio antes de crear pedido
4. POST /api/pedidos/              → crear pedido (precio calculado solo)
5. POST /api/pagos/                → registrar abono
6. PATCH /api/pedidos/1/           → cambiar estado a en_proceso / terminado
7. GET  /api/pagos/deudas/         → verificar si quedó saldo pendiente
