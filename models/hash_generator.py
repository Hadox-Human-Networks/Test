from werkzeug.security import generate_password_hash, check_password_hash

print(generate_password_hash('user1'))

print(check_password_hash('pbkdf2:sha256:260000$lXf396gTFrOlFVi3$0486e4ee786d539f5b8145d959739489f7f2c6f28d247fdcbc7b6797168b6123', 'user1'))
