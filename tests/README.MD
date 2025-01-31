# 📌 Pruebas en Delivery-Nono-Backend  

Este documento describe el proceso de pruebas en el backend del proyecto **Delivery Nono**, incluyendo la configuración, ejecución y descripción de los tests implementados.  

## 📂 Estructura de pruebas  

Las pruebas unitarias y de integración se encuentran en el directorio `tests/`, que tiene la siguiente estructura:  


tests/
│── test_database_connection.py  # Pruebas para la conexión a la base de datos
│── pedido_test.py               # Pruebas para la gestión de pedidos

## ⚙️ Configuración antes de ejecutar los tests  

1. **Instalar dependencias**  

   pip install -r requirements.txt

2. **Crear un archivo de configuración de pruebas**  

   Se usa un archivo `.env.test` para configurar la base de datos de testing. Crea este archivo en la raíz del proyecto con el siguiente contenido:  

   DATABASE_USERNAME=root
   DATABASE_PASSWORD=tu_contraseña
   DATABASE_HOST=127.0.0.1
   DATABASE_PORT=3306
   DATABASE_NAME=nono_test

3. **Verificar que la base de datos de pruebas existe**  
   Antes de ejecutar las pruebas, asegúrate de que la base de datos `nono_test` está creada en MySQL:  

   CREATE DATABASE nono_test;

## 🧪 Cómo ejecutar las pruebas  

Para correr todas las pruebas, usa el siguiente comando:  

pytest -s

Para ejecutar un test en específico, por ejemplo `pedido_test.py`, usa:  

pytest tests/pedido_test.py -s

Si quieres ver un informe detallado de las pruebas, puedes ejecutar:  

pytest -v

## 📌 Pruebas implementadas  

### ✅ Prueba de conexión a la base de datos  
Archivo: `tests/test_database_connection.py`  

- Verifica que la conexión con la base de datos se establece correctamente.  
- Confirma que la configuración se carga desde las variables de entorno.  

### ✅ Pruebas para pedidos  
Archivo: `tests/pedido_test.py`  

- **`test_create_pedido`**: Verifica que se puede crear un pedido correctamente.  
- **`test_configuracion_correcta`**: Comprueba que las variables de entorno se cargan correctamente.  
