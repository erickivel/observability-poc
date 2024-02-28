from flask import Blueprint, jsonify, request
import psycopg2

from src.db import get_db_connection

product_orders_bp = Blueprint('product_orders', __name__, url_prefix="/product_orders")

@product_orders_bp.route('/', methods=['POST'])
def create_product_order():
    print("Creating product_order")
    connection = get_db_connection()

    if connection:
        cursor = connection.cursor()
        try:
            data = request.get_json()

            if data is None:
                return jsonify({"error": "Request body is null"}), 403

            cursor.execute("""
                INSERT INTO product_orders (quantity, product_id, order_id) 
                VALUES (%s, %s, %s)
                RETURNING *;
            """, 
                (data["quantity"], data["product_id"], data["order_id"])
            )

            connection.commit()

            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            res = [{column_names[i]: row[i] for i in range(len(row))} for row in rows][0]

            print(f"product_order '{rows[0][0]}' created successfully!")
            return jsonify(res), 201
        except psycopg2.Error as e:
            print("Error executing query:", e)
            return jsonify({"error": "Error when creating order"}), 500
        finally:
            cursor.close()
            connection.close()

    return jsonify({"error": "Error when connecting to database"}), 500

@product_orders_bp.route('/', methods=['GET'])
def list_product_orders():
    print("Fetching product_orders")
    connection = get_db_connection()

    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT * FROM product_orders
                ORDER BY id DESC
                LIMIT 100
            """
           )

            connection.commit()

            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            res = [{column_names[i]: row[i] for i in range(len(row))} for row in rows]


            print("product_orders fetched successfully!")
            return jsonify(res)
        except psycopg2.Error as e:
            print("Error executing query:", e)
            return jsonify({"error": "Error when creating order"}), 500
        finally:
            cursor.close()
            connection.close()

    return jsonify({"error": "Error when connecting to database"}), 500
