SELECT_ALL_FILES = """
    SELECT * FROM files 
    WHERE user_id = :user_id; 
"""

SELECT_FILE = """
    SELECT * FROM files WHERE filename = :filename and user_id = :user_id; 
"""

INSERT_FILE = """
    INSERT into files (user_id, filename, metadata)
    VALUES (:user_id, :filename, :metadata)
    RETURNING file_id, uploaded_at; 
"""

INSERT_USER = """
    INSERT into users (name, email, password_hash) 
    VALUES (:name, :email, :password_hash) 
    RETURNING id, created_at 
"""

SELECT_USER_BY_EMAIL = """
    SELECT * FROM users 
    WHERE email = :email
"""