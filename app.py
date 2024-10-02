from flask import Flask, request, jsonify
from datetime import datetime
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Use environment variables for configuration
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'blog_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')  # This line reads the password
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'blog_api')

mysql = MySQL(app)

@app.route("/posts", methods=['POST'])
def create():
    data = request.json
    if not all([data['title'], data['content'], data['category']]):
        return jsonify({"error": "Title, content, and category are required"}), 400
    
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO posts (title, content, category, tags)
        VALUES (%s, %s, %s, %s)
    """, 
        (data['title'], 
         data['content'], 
         data['category'], 
         ','.join(data.get('tags', []))
    ))

    mysql.connection.commit()
    new_id = cur.lastrowid
    
    # Fetch the newly created post
    cur.execute("SELECT * FROM posts WHERE id = %s", (new_id,))
    new_post = cur.fetchone()
    columns = [column[0] for column in cur.description]
    cur.close()
    
    post_dict = dict(zip(columns, new_post))
    return jsonify(post_dict), 201

@app.route("/posts/<int:id>", methods=['PUT'])
def update(id):
    data = request.json
    required_fields = ['title', 'content', 'category']
    if not any(field in data for field in required_fields):
        return jsonify({"error": "At least one of title, content, and category is required"}), 400
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE posts SET title = %s, content= %s, category= %s, tags= %s, updatedAt =%s
                WHERE id = %s """,
                (data['title'], 
                 data['content'], 
                 data['category'], 
                 ','.join(data.get('tags', [])),
                 datetime.now().isoformat(),
                 id
    ))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()  
    if affected_rows == 0:
        return jsonify({"error": "Post not found"}), 404
    
    return jsonify({
            "id":id,
            "title": data['title'],
            "content": data['content'],
            "category": data['category'],
            "tags": data.get('tags', []),
            "updatedAt": datetime.now().isoformat() + "Z"
    }), 200

@app.route("/posts/<int:id>", methods=['DELETE'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM posts WHERE id =%s", (id,))
    affected_rows = cur.rowcount
    mysql.connection.commit()
    cur.close()
    if affected_rows > 0:
        return jsonify({"message": "Post deleted successfully"}), 204
    return jsonify({'error': "Post not found"}), 404

@app.route("/posts/<int:id>", methods=["GET"])
def get(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cur.fetchone()
    if post:
        columns = [column[0] for column in cur.description]
        cur.close()
        post_dict = dict(zip(columns, post))
        return jsonify(post_dict), 200
    else:
        cur.close()
        return jsonify({"error": "Post not found"}), 404

@app.route("/posts", methods=["GET"])
def all_post():
    cur = mysql.connection.cursor()
    search_term = request.args.get('term', '').lower()
    if search_term:
        query = """SELECT * FROM posts 
                WHERE LOWER(title) LIKE %s 
                OR LOWER(content) LIKE %s 
                OR LOWER(category) LIKE %s"""
        search_pattern = f"%{search_term}%"
        cur.execute(query, (search_pattern, search_pattern, search_pattern))             
    else:
        cur.execute("SELECT * FROM posts")
    
    columns = [column[0] for column in cur.description]
    posts = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return jsonify(posts), 200
if __name__ == "__main__":
    app.run(debug=True)