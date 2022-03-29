# Урок 19 - Декораторы и контроль доступа

### 1 Создание модели и схемы пользователя

#### 1.1 Модель
	class User(db.Model):
		__tablename__ = 'user'
		id = db.Column(db.Integer, primary_key=True)
		username = db.Column(db.String)
		password = db.Column(db.String)
		role = db.Column(db.String)

#### 1.2 Для модели определены views с методами GET/POST/PUT/DELETE

#### 2.1 Создание пользователей в БД  (файл movies.db) через create_data
	def create_data(app, db):
    	with app.app_context():
	        db.create_all()
	        u1 = User(username="vasya", password="my_little_pony", role="user")
    	    u2 = User(username="oleg", password="qwerty", role="user")
        	u3 = User(username="oleg", password="P@ssw0rd", role="admin")
	        with db.session.begin():
    	        db.session.add_all([u1, u2, u3])

#### 2.2 Метод генерации хеша пароля пользователя реализован с помощью md5

	def get_hash(self):
		return hashlib.md5(self.password.encode('utf-8')).hexdigest()

### 3. У моделей Director и Genre определены методы POST, PUT, DELETE

### 4. Эндпоинты аутентификации:
	(кто угодно) 
	`POST` /auth/ — возвращает access_token и refresh_token или 401 
			получает логин и пароль из Body запроса в виде JSON, 
			далее проверяет соотвествие с данными в БД (есть ли такой пользователь, 
			такой ли у него пароль) и если всё оk — генерит пару access_token и refresh_token
			и отдает их в виде JSON.

	`PUT` /auth/ — возвращает access_token и refresh_token или 401
			получает refresh_token из Body запроса в виде JSON, далее проверяет 
			refresh_token и если он не истек и валиден — генерит пару access_token и refresh_token
			и отдает их в виде JSON.

### 5. Ограничение доступа на чтение
	(Authorized Required):
		`GET` /directors/ + /directors/id
		`GET` /movies/ + /movies/id
		`GET` /genres/ + /genres/id

### 6. Ограничение доступа на редактирование
	(Admin Required):
		`POST/PUT/DELETE`  /movies/ + /movies/id
		`POST/PUT/DELETE`  /genres/ + /genres/id
		`POST/PUT/DELETE`  /directors/ + /directors/id

### 7. Регистрация пользователя
	`POST` /users/ — создает пользователя
		Пример запроса (кто угодно):
			POST /users/
			{
				"username": "ivan",
				"password": "qwerty",
				"role": "admin"
			}