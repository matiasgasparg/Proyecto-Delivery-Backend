from flask import request, jsonify
from ..models.plato_model import Plato
from ..models.exceptions import CustomException, InvalidDataError, ProductNotFound, DuplicateError

class PlatoController:
    """
    Controlador para manejar las operaciones CRUD relacionadas con los platos.

    Métodos:
        - `get`: Obtener un plato específico por su ID.
        - `get_all`: Obtener todos los platos disponibles.
        - `create`: Crear un nuevo plato.
        - `update`: Actualizar un campo específico de un plato existente.
        - `delete`: Eliminar un plato por su ID.
    """

    @classmethod
    def get(cls, id_plato):
        """
        Obtiene los detalles de un plato específico por su ID.

        Args:
            id_plato (int): ID del plato a obtener.

        Returns:
            tuple: JSON con los datos del plato y el código de estado HTTP.
        """
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
                raise ProductNotFound(id_plato)  # Lanzar excepción si el plato no existe.
        except ProductNotFound as e:
            return e.get_response()  # Respuesta personalizada para plato no encontrado.
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def get_all(cls):
        """
        Obtiene todos los platos disponibles.

        Returns:
            tuple: JSON con la lista de platos y el código de estado HTTP.
        """
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
        """
        Crea un nuevo plato.

        El cuerpo de la solicitud debe incluir:
            - `nombre` (str): Nombre del plato.
            - `descripcion` (str, opcional): Descripción del plato.
            - `precio` (float): Precio del plato.
            - `disponible` (bool): Indica si el plato está disponible.

        Returns:
            tuple: JSON con un mensaje y el código de estado HTTP.
        """
        try:
            data = request.json
            if not data.get('nombre') or not isinstance(data.get('precio'), (int, float)):
                raise InvalidDataError("El campo 'nombre' es obligatorio y 'precio' debe ser un número válido.")
            
            new_plato = Plato(**data)
            if Plato.create(new_plato):
                return jsonify({'message': 'Plato creado exitosamente'}), 201
            else:
                raise DuplicateError("Ya existe un plato con los mismos datos.")
        except InvalidDataError as e:
            return e.get_response()
        except DuplicateError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def update(cls, id_plato):
        """
        Actualiza un campo específico de un plato existente.

        Args:
            id_plato (int): ID del plato a actualizar.

        El cuerpo de la solicitud debe incluir:
            - `field` (str): Campo a actualizar (nombre, descripcion, precio, disponible).
            - `value` (any): Nuevo valor para el campo.

        Returns:
            tuple: JSON con un mensaje y el código de estado HTTP.
        """
        try:
            # Verificar si el plato existe
            plato = Plato.get(id_plato)
            if not plato:
                raise ProductNotFound(id_plato)  # Lanza un error si no existe el plato

            # Si el plato existe, proceder con la actualización
            data = request.json
            field_to_update = data.get('field')
            value = data.get('value')
            valid_fields = ['nombre', 'descripcion', 'precio', 'disponible']

            if field_to_update not in valid_fields:
                raise InvalidDataError(f"'{field_to_update}' no es un campo válido para actualizar.")

            response = Plato.update(id_plato, field_to_update, value)
            return jsonify({'message': response}), 200
        except ProductNotFound as e:
            return e.get_response()  # Respuesta personalizada para plato no encontrado.
        except InvalidDataError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def delete(cls, id_plato):
        """
        Elimina un plato por su ID.

        Args:
            id_plato (int): ID del plato a eliminar.

        Returns:
            tuple: JSON con un mensaje y el código de estado HTTP.
        """
        try:
            plato=Plato.get(id_plato)
            if not plato:
                raise ProductNotFound(f"Plato con ID {id_plato} no encontrado.")
            response, status_code = Plato.delete(id_plato)
            return jsonify(response), status_code
        except ProductNotFound as e:
            return e.get_response()  # Respuesta personalizada para plato no encontrado.
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
