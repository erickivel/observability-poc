from flask import Blueprint, jsonify, request
import psycopg2

from db import get_db_connection

orders_bp = Blueprint('orders', __name__, url_prefix="/orders")

@orders_bp.route('/', methods=['POST'])
def create_order():
    print("Creating order")
    connection = get_db_connection()

    if connection:
        cursor = connection.cursor()
        try:
            data = request.get_json()

            if data is None:
                return jsonify({"error": "Request body is null"}), 403

            cursor.execute("""
                INSERT INTO orders (user_id, total_value) 
                VALUES (%s, %s)
                RETURNING *;
            """, 
                (data["user_id"], data["total_value"])
           )

            connection.commit()

            row = cursor.fetchall()[0]
            res = {
                "id": row[0],
                "total_value": row[1],
                "user_id": row[2],
                "created_at": row[3],
                "updated_at": row[4],
            }

            print(f"Order '{row[0]}' created successfully!")
            return jsonify(res), 201
        except psycopg2.Error as e:
            print("Error executing query:", e)
            return jsonify({"error": "Error when creating order"}), 500
        finally:
            cursor.close()
            connection.close()

    return jsonify({"error": "Error when connecting to database"}), 500

@orders_bp.route('/', methods=['GET'])
def list_orders():
    print("Fetching orders")
    connection = get_db_connection()

    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT * FROM orders
                ORDER BY id DESC
                LIMIT 100
            """
            )

            connection.commit()

            rows = cursor.fetchall()
            res = [{"id": t[0], "total_value": t[1],"user_id": t[2], "created_at": t[3], "updated_at": t[4]} for t in rows]

            print("Orders fetched successfully!")
            return jsonify(res)
        except psycopg2.Error as e:
            print("Error executing query:", e)
            return jsonify({"error": "Error when creating order"}), 500
        finally:
            cursor.close()
            connection.close()

    return jsonify({"error": "Error when connecting to database"}), 500
