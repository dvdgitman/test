import os
import psycopg2
from flask import Flask, request, jsonify
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database Configuration (Secrets injected via Env Vars)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "audiodb")
DB_USER = os.getenv("DB_USER", "dbadmin")
DB_PASS = os.getenv("DB_PASSWORD", "secret")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/features', methods=['GET'])
def get_features():
    """
    Retrieves features based on time range.
    Query Params: sensor_id, start_time, end_time
    """
    sensor_id = request.args.get('sensor_id')
    
    # Basic validation
    if not sensor_id:
        return jsonify({"error": "sensor_id is required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # SQL Injection safe query using parameters
        query = """
            SELECT * FROM features 
            WHERE sensor_id = %s 
            LIMIT 100
        """
        cur.execute(query, (sensor_id,))
        rows = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify(rows), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
