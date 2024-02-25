from flask import Blueprint, jsonify, request
import psycopg2

from db import get_db_connection

products_bp = Blueprint('products', __name__, url_prefix="/products")

@products_bp.route('/', methods=['POST'])
def create_product():
    connection = get_db_connection()

    if connection:
        cursor = connection.cursor()
        try:
            data = request.get_json()

            if data is None:
                return jsonify({"error": "Request body is null"}), 403

            cursor.execute("""
                INSERT INTO products (name, value) 
                VALUES (%s, %s)
                RETURNING id, name, value;
            """, 
                (data["name"], data["value"])
           )

            connection.commit()

            row = cursor.fetchall()[0]
            res = {
                "id": row[0],
                "name": row[1],
                "value": row[2]
            }

            return jsonify(res)
        except psycopg2.Error as e:
            print("Error executing query:", e)
        finally:
            cursor.close()
            connection.close()

    return jsonify({"error": "Error when connecting to database"}), 500

@products_bp.route('/', methods=['GET'])
def list_products():
    connection = get_db_connection()

    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT * FROM products
                ORDER BY id DESC
                LIMIT 100
            """
           )

            connection.commit()

            rows = cursor.fetchall()
            res = [{"id": t[0], "name": t[1], "value": t[2]} for t in rows]

            return jsonify(res)
        except psycopg2.Error as e:
            print("Error executing query:", e)
        finally:
            cursor.close()
            connection.close()

    return jsonify({"error": "Error when connecting to database"}), 500
