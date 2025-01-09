from flask import Flask, request, jsonify
from ..models.plato_model import Plato
from flask_cors import CORS
from ..models.exceptions import CustomException, InvalidDataError, ProductNotFound, DuplicateError

class PlatoController:
    @classmethod
    def get(cls, id_plato):
        try:
            plato = Plato.get(id_plato)
            if plato:
                serialized_plato = {
                    "id_plato": plato.id_plato,
                    "nombre": plato.nombre,
                    "descripcion": plato.descripcion,
                    "precio": plato.precio,
                    "disponible": plato.disponible
                }
                return jsonify(serialized_plato), 200
            else:
                raise ProductNotFound(id_plato)  # Si el plato no se encuentra, lanzar excepción
        except ProductNotFound as e:
            return e.get_response()  # Usar el método get_response de la excepción personalizada
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def get_all(cls):
        try:
            platos = Plato.get_all()
            serialized_platos = [
                {
                    "id_plato": plato.id_plato,
                    "nombre": plato.nombre,
                    "descripcion": plato.descripcion,
                    "precio": plato.precio,
                    "disponible": plato.disponible
                } for plato in platos
            ]
            return jsonify(serialized_platos), 200
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def create(cls):
        try:
            data = request.json
            if not data.get('nombre') or not isinstance(data.get('precio'), (int, float)):
                raise InvalidDataError("El campo 'nombre' es obligatorio y 'precio' debe ser un número válido.")
            
            new_plato = Plato(**data)
            if Plato.create(new_plato):
                return jsonify({'message': 'Plato creado exitosamente'}), 201
            else:
                raise duplicateError("Ya existe un plato con los mismos datos.")
        except InvalidDataError as e:
            return e.get_response()
        except duplicateError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def update(cls, id_plato):
        try:
            data = request.json
            field_to_update = data.get('field')
            value = data.get('value')
            valid_fields = ['nombre', 'descripcion', 'precio', 'disponible']

            if field_to_update not in valid_fields:
                raise InvalidDataError(f"'{field_to_update}' no es un campo válido para actualizar.")

            response = Plato.update(id_plato, field_to_update, value)
            return jsonify({'message': response}), 200
        except ProductNotFound as e:
            return e.get_response()
        except InvalidDataError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def delete(cls, id_plato):
        try:
            response, status_code = Plato.delete(id_plato)
            return jsonify(response), status_code
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
