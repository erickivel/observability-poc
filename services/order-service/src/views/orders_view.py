from flask import Blueprint, jsonify, request
from flask import current_app as app
import psycopg2

from src.db import get_db_connection

orders_bp = Blueprint('orders', __name__, url_prefix="/orders")

@orders_bp.route('/', methods=['POST'])
def create_order():
    app.logger.info("Creating order")
    connection = get_db_connection()

    if connection:
        cursor = connection.cursor()
        try:
            data = request.get_json()

            if data is None:
                return jsonify({"error": "Request body is null"}), 403

            cursor.execute("""
                INSERT INTO orders (user_id) 
                VALUES (%s)
                RETURNING *;
            """, 
                (data["user_id"])
           )

            connection.commit()

            row = cursor.fetchall()[0]
            res = {
                "id": row[0],
                "user_id": row[1],
                "created_at": row[2],
                "updated_at": row[3],
            }

            app.logger.info(f"Order '{row[0]}' created successfully!")
            return jsonify(res), 201
        except psycopg2.Error as e:
            app.logger.error("Error executing query: %s", e)
            return jsonify({"error": "Error when creating order"}), 500
        finally:
            cursor.close()
            connection.close()

    return jsonify({"error": "Error when connecting to database"}), 500

@orders_bp.route('/', methods=['GET'])
def list_orders():
    app.logger.info("Fetching orders")
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
            res = [{"id": t[0], "user_id": t[1], "created_at": t[2], "updated_at": t[3]} for t in rows]

            app.logger.info("Orders fetched successfully!")
            return jsonify(res)
        except psycopg2.Error as e:
            app.logger.error("Error executing query: %s", e)
            return jsonify({"error": "Error when listing orders"}), 500
        finally:
            cursor.close()
            connection.close()

    return jsonify({"error": "Error when connecting to database"}), 500

@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    order_id = int(order_id)
    app.logger.info(f"Fetching order '{order_id}'")
    connection = get_db_connection()

    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                SELECT 
                    o.id AS order_id,
                    o.created_at AS order_created_at,
                    o.updated_at AS order_updated_at,
                    u.id AS user_id,
                    u.name AS user_name,
                    u.email AS user_email,
                    u.phone AS user_phone,
                    po.id AS product_order_id,
                    po.quantity AS product_order_quantity,
                    po.created_at AS product_order_created_at,
                    po.updated_at AS product_order_updated_at,
                    p.id AS product_id,
                    p.name AS product_name,
                    p.value AS product_value
                FROM 
                    orders o
                JOIN 
                    users u ON o.user_id = u.id
                JOIN 
                    product_orders po ON o.id = po.order_id
                JOIN 
                    products p ON po.product_id = p.id
                WHERE 
                    o.id = {order_id};
            """
            )


            connection.commit()

            rows = cursor.fetchall()

            if len(rows) == 0:
                return jsonify([])

            order_data = {}

            # Iterate over the rows and organize data into dictionary
            for row in rows:
                order_id = row[0]
                order_info = {
                    "id": row[0],
                    "created_at": row[1],
                    "updated_at": row[2],
                    "user": {
                        "id": row[3],
                        "name": row[4],
                        "email": row[5],
                        "user_phone": row[6]
                    },
                    "product_orders": []
                }

                # Check if the order is already in the dictionary
                if "order" not in order_data:
                    order_data["order"] = order_info

                # Append product order info to the order
                product_order_info = {
                    "id": row[7],
                    "quantity": row[8],
                    "created_at": row[9],
                    "updated_at": row[10],
                    "product": {
                        "id": row[11],
                        "name": row[12],
                        "value": row[13]
                    }
                }
                order_data["order"]["product_orders"].append(product_order_info)

            app.logger.info(f"Order '{order_id}' fetched successfully!")
            return jsonify(order_data)
        except psycopg2.Error as e:
            app.logger.error("Error executing query: %s", e)
            return jsonify({"error": "Error when fetching order"}), 500
        finally:
            cursor.close()
            connection.close()

    return jsonify({"error": "Error when connecting to database"}), 500
