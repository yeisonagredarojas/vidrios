# 🪟 ERP Vidrios — Sistema de Gestión Empresarial

Sistema ERP completo para empresas de vidrios, desarrollado con **Django 5 + PostgreSQL + Docker**.
Reemplaza Excel, WhatsApp manual y procesos en papel con una plataforma digital moderna.

---

## 🚀 Inicio Rápido (Docker)

```bash
# 1. Clonar / descomprimir el proyecto
cd vidrios_erp

# 2. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus datos

# 3. Construir y arrancar
cd docker
docker-compose up --build -d

# 4. Inicializar datos base (solo la primera vez)
docker exec vidrios_web python manage.py setup_inicial

# 5. Abrir el sistema
# Dashboard:    http://localhost:8000/dashboard/
# Sitio público: http://localhost:8000/inicio/
# Admin Django: http://localhost:8000/admin/
# Usuario: admin | Contraseña: admin123
```

---

## 🏗️ Sin Docker (Desarrollo Local)

```bash
# Requisitos: Python 3.12+, PostgreSQL 15+

pip install -r requirements.txt

# Crear base de datos PostgreSQL
createdb vidrios_db

# Configurar .env (apuntar DB_HOST a localhost)
cp .env.example .env

# Migraciones
python manage.py migrate

# Datos iniciales
python manage.py setup_inicial

# Servidor de desarrollo
python manage.py runserver
```

---

## 📦 Módulos del Sistema

| Módulo | URL | Descripción |
|--------|-----|-------------|
| **Dashboard** | `/dashboard/` | KPIs, gráficas, últimos pedidos |
| **Clientes** | `/clientes/` | CRUD + estado financiero |
| **Pedidos** | `/pedidos/` | Pedidos con cotización automática |
| **Pagos** | `/pagos/` | Registro de pagos y deudas |
| **Inventario** | `/inventario/` | Stock con alertas de bajo inventario |
| **Cotizaciones** | `/cotizaciones/` | Configuración de precios parametrizable |
| **Trabajadores** | `/trabajadores/` | Personal y roles |
| **Proveedores** | `/proveedores/` | Gestión de proveedores |
| **Sitio Público** | `/inicio/` | Landing page + cotizador online |
| **API REST** | `/api/` | Endpoints JSON para integraciones |

---

## 📐 Reglas de Negocio Implementadas

- **Vidrio Normal**: Máximo 2.14m × 3.30m
- **Vidrio Tallado / Figuritas**: Máximo 1.83m × 2.44m
- **Espejos**: Espesor estándar 3mm
- **Cotización automática**: precio = área × precio_m² + recargo_trabajo + transporte
- **Estado financiero**: Paz y Salvo / Con Deuda (calculado automáticamente)
- **Inventario**: Alertas cuando stock ≤ stock_mínimo

---

## 🔌 API REST

```
GET/POST  /api/clientes/
GET/POST  /api/pedidos/
GET/POST  /api/pagos/
GET/POST  /api/inventario/
POST      /api/cotizaciones/calcular/   ← Cotización pública sin auth
```

**Ejemplo cotización:**
```bash
curl -X POST http://localhost:8000/api/cotizaciones/calcular/ \
  -H "Content-Type: application/json" \
  -d '{"tipo_vidrio":"normal","ancho":1.5,"alto":2.0,"tipo_trabajo":"corte","es_envio_nacional":false}'
```

---

## 🏗️ Arquitectura

```
vidrios_erp/
├── apps/
│   ├── clientes/          # Gestión de clientes
│   ├── pedidos/           # Pedidos + notificaciones
│   ├── pagos/             # Pagos y control de deudas
│   ├── inventario/        # Stock de materiales
│   ├── cotizaciones/      # Precios configurables + servicio de cálculo
│   ├── trabajadores/      # Personal
│   └── proveedores/       # Proveedores
├── core/
│   ├── settings.py        # Configuración Django
│   ├── urls.py            # URLs principales
│   ├── views.py           # Dashboard + landing
│   └── management/commands/setup_inicial.py
├── templates/             # Templates HTML Bootstrap 5
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── nginx/nginx.conf
├── requirements.txt
└── .env.example
```

---

## ⚙️ Variables de Entorno (.env)

| Variable | Descripción | Defecto |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta Django | ⚠ Cambiar en producción |
| `DEBUG` | Modo debug | `True` |
| `DB_*` | Conexión PostgreSQL | Ver .env.example |
| `EMAIL_*` | Configuración SMTP | Console backend |
| `WHATSAPP_API_TOKEN` | Token API WhatsApp Business | Vacío (mock) |
| `EMPRESA_NOMBRE` | Nombre de la empresa | Editable |

---

## 📱 WhatsApp

Si `WHATSAPP_API_TOKEN` está vacío, el sistema opera en **modo mock** y solo loguea los mensajes en consola. Para activar WhatsApp real, configura una cuenta en [Meta for Developers](https://developers.facebook.com/docs/whatsapp).

---

## 🔒 Seguridad para Producción

1. Cambiar `SECRET_KEY` y `DEBUG=False`
2. Cambiar contraseña del admin
3. Configurar `ALLOWED_HOSTS` con tu dominio
4. Usar HTTPS (configurar en Nginx o en el proveedor cloud)
5. Configurar variables de entorno en el servidor (no en .env)

---

## ☁️ Despliegue en la Nube

**Railway/Render:** Soportan Docker directamente. Apunta al `docker/Dockerfile`.

**VPS (Ubuntu):**
```bash
apt install docker.io docker-compose
git clone <tu-repo>
cd vidrios_erp/docker
docker-compose up -d
```

**AWS ECS/EB:** Usa el `Dockerfile` con las variables de entorno de RDS para PostgreSQL.

