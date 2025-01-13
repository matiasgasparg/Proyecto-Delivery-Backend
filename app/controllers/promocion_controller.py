from flask import request, jsonify
from ..models.promocion_model import Promocion
from ..models.plato_model import Plato

class PromocionController:

    @classmethod
    def create(cls):
        try:
            data = request.json

            # Validar que el plato es válido
            plato_id = data.get('plato')
            if plato_id:
                plato = Plato.get(plato_id)
                if not plato:
                    return jsonify({"error": "Plato no encontrado."}), 404

            # Crear la promoción con el plato
            nueva_promocion = Promocion(**data)
            if not Promocion.create(nueva_promocion):
                return jsonify({"error": "No se pudo crear la promoción."}), 400
            return jsonify({"message": "Promoción creada exitosamente."}), 201
        except Exception as e:
            print("Error inesperado al crear promoción:", e)
            return jsonify({"error": "Error inesperado", "details": str(e)}), 500

    @classmethod
    def get_all(cls):
        try:
            promociones = Promocion.get_all()
            serialized_promociones = []

            for promocion in promociones:
                # Serializar cada promoción
                serialized_promocion = {
                    "id_promocion": promocion.id_promocion,
                    "tipo": promocion.tipo,
                    "descripcion": promocion.descripcion,
                    "monto_minimo": promocion.monto_minimo,
                    "descuento_porcentaje": promocion.descuento_porcentaje,
                    "precio": promocion.precio,
                    "disponible": promocion.disponible,
                    "id_plato": promocion.id_plato  # Agregamos solo el id_plato
                }

                # Si la promoción tiene un plato asociado, serializamos los detalles del plato
                if promocion.plato:
                    serialized_promocion["plato"] = {
                        "id_plato": promocion.plato.id_plato,
                        "nombre": promocion.plato.nombre,
                        "descripcion": promocion.plato.descripcion,
                        "precio": promocion.plato.precio,
                        "tipo_plato": promocion.plato.tipo_plato,
                        "disponible": promocion.plato.disponible
                    }

                serialized_promociones.append(serialized_promocion)

            return jsonify(serialized_promociones), 200

        except Exception as e:
            print(f"Error al obtener promociones: {str(e)}")
            return jsonify({'error': 'Error inesperado al obtener promociones', 'details': str(e)}), 500