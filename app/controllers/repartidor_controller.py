from flask import request, jsonify
from ..models.repartidor_model import Repartidor
from ..models.exceptions import CustomException, InvalidDataError, ProductNotFound, DuplicateError
from werkzeug.security import check_password_hash

class RepartidorController:
    @classmethod
    def login(cls):
        try:
            data = request.json
            telefono = data.get('telefono')
            contraseña = data.get('contraseña')

            if not telefono or not contraseña:
                raise InvalidDataError("telefono y contraseña son obligatorios.")
    
            repartidor = Repartidor.get_by_telefono(telefono)
            if repartidor and check_password_hash(repartidor.contraseña, contraseña):
                # Devolver el id_repartidor y otros datos que quieras incluir
                return jsonify({
                    'message': 'Login exitoso',
                    'id_repartidor': repartidor.id_repartidor,  # Usando id_repartidor en lugar de id
                    'telefono': repartidor.telefono,
                    # Agregar otros datos que consideres necesarios
                    'nombre': repartidor.nombre,
                    'disponible': repartidor.disponible,
                }), 200
            else:
                return jsonify({'error': 'Telefono o contraseña incorrectos'}), 401
        except InvalidDataError as e:
            return e.get_response()
        except Exception as e:
            print("Error al procesar la solicitud:", e)
            return jsonify({'error': f'Error en la solicitud: {str(e)}'}), 500


    @classmethod
    def get(cls, id_repartidor):
        try:
            repartidor = Repartidor.get(id_repartidor)
            if repartidor:
                serialized_repartidor = {
                    "id_repartidor": repartidor.id_repartidor,
                    "nombre": repartidor.nombre,
                    "telefono": repartidor.telefono,
                    "disponible": repartidor.disponible  # Incluyendo el campo disponible
                }
                return jsonify(serialized_repartidor), 200
            else:
                raise ProductNotFound(id_repartidor)
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def get_all(cls):
        try:
            repartidores = Repartidor.get_all()
            serialized_repartidores = [
                {
                    "id_repartidor": repartidor.id_repartidor,
                    "nombre": repartidor.nombre,
                    "telefono": repartidor.telefono,
                    "disponible": repartidor.disponible  # Incluyendo el campo disponible
                } for repartidor in repartidores
            ]
            return jsonify(serialized_repartidores), 200
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
    @classmethod
    def create(cls):
        try:
            data = request.json
            nombre = data.get('nombre')
            telefono = data.get('telefono')
            disponible=data.get('disponible')

            contraseña = data.get('contraseña')

            if not telefono or not contraseña:
                raise InvalidDataError("telefono y contraseña son obligatorios.")

            new_repartidor = Repartidor(nombre=nombre, telefono=telefono,disponible=disponible, contraseña=contraseña)
            if Repartidor.create(new_repartidor):
                return jsonify({'message': 'repartidor creado exitosamente'}), 201
            else:
                return jsonify({'error': 'Error al crear el Repartidor'}), 500
        except InvalidDataError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
    @classmethod
    def update(cls, id_repartidor):
        try:
            data = request.json
            field_to_update = data.get('field')
            value = data.get('value')
            valid_fields = ['nombre', 'telefono', 'disponible']  # Agregando 'disponible' como campo actualizable

            if field_to_update not in valid_fields:
                raise InvalidDataError(f"'{field_to_update}' no es un campo válido para actualizar.")

            response = Repartidor.update(id_repartidor, field_to_update, value)
            print(value)
            return jsonify({'message': response}), 200
        except ProductNotFound as e:
            return e.get_response()
        except InvalidDataError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def delete(cls, id_repartidor):
        try:
            repartidor = Repartidor.get(id_repartidor)
            if not repartidor:
                raise ProductNotFound(f"Repartidor con ID {id_repartidor} no encontrado.")
            
            response, status_code = Repartidor.delete(id_repartidor)
            return jsonify(response), status_code
        except ProductNotFound as e:
            return e.get_response()  # Devolver 404 con el mensaje de error adecuado
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
    @classmethod
    def get_available(cls):
       try:
           disponibles = request.args.get('disponible', default=1, type=int)  # Obtén el valor de 'disponible' de los parámetros de consulta
           repartidores = Repartidor.get_by_disponibilidad(disponibles)
    
           serialized_repartidores = [
               {
                   "id_repartidor": repartidor.id_repartidor,
                   "nombre": repartidor.nombre,
                   "telefono": repartidor.telefono,
                   "disponible": repartidor.disponible
               } for repartidor in repartidores
           ]
    
           return jsonify(serialized_repartidores), 200
       except Exception as e:
           print("Error al obtener repartidores disponibles:", e)
           return jsonify({'error': 'Error en la solicitud'}), 500
