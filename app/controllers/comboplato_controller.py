from flask import request, jsonify
from ..models.comboplato_model import ComboPlato
from ..models.exceptions import CustomException, InvalidDataError, ProductNotFound, DuplicateError

class ComboPlatoController:
    @classmethod
    def get(cls, id_combo_plato):
        try:
            combo_plato = ComboPlato.get(id_combo_plato)
            if combo_plato:
                serialized_combo_plato = {
                    "id_combo_plato": combo_plato.id_combo_plato,
                    "id_promocion": combo_plato.id_promocion,
                    "id_plato": combo_plato.id_plato
                }
                return jsonify(serialized_combo_plato), 200
            else:
                raise ProductNotFound(id_combo_plato)
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def get_all(cls):
        try:
            combos_plato = ComboPlato.get_all()
            serialized_combos_plato = [
                {
                    "id_combo_plato": combo_plato.id_combo_plato,
                    "id_promocion": combo_plato.id_promocion,
                    "id_plato": combo_plato.id_plato
                } for combo_plato in combos_plato
            ]
            return jsonify(serialized_combos_plato), 200
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def create(cls):
        try:
            data = request.json
            if not data.get('id_promocion') or not data.get('id_plato'):
                raise InvalidDataError("El id_promocion y el id_plato son obligatorios.")

            new_combo_plato = ComboPlato(**data)
            if ComboPlato.create(new_combo_plato):
                return jsonify({'message': 'Combo creado exitosamente'}), 201
            else:
                raise DuplicateError("Ya existe un combo con los mismos datos.")
        except InvalidDataError as e:
            return e.get_response()
        except DuplicateError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def update(cls, id_combo_plato):
        try:
            data = request.json
            field_to_update = data.get('field')
            value = data.get('value')
            valid_fields = ['id_promocion', 'id_plato']

            if field_to_update not in valid_fields:
                raise InvalidDataError(f"'{field_to_update}' no es un campo válido para actualizar.")

            response = ComboPlato.update(id_combo_plato, field_to_update, value)
            return jsonify({'message': response}), 200
        except ProductNotFound as e:
            return e.get_response()
        except InvalidDataError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def delete(cls, id_combo_plato):
        try:
            response, status_code = ComboPlato.delete(id_combo_plato)
            return jsonify(response), status_code
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
