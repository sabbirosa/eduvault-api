# EduVault API

EduVault is an API designed to manage and share educational resources. Users can register, login, create resources, save/unsave resources, and view their own created resources.

## Base URL

All endpoints are relative to the base URL:

https://eduvault.sabbir.co/api/

## API Endpoints

### Home Route

**GET /**

Welcome message for the API.

```bash
curl -X GET https://eduvault.sabbir.co/api/
```

##### Response:

```json
{
  "message": "Welcome to EduVault!"
}
```

### User Registration

**POST /register**

Register a new user.

```bash
curl -X POST https://eduvault.sabbir.co/api/register \
-H "Content-Type: application/json" \
-d '{
  "full_name": "John Doe",
  "student_id": "123456",
  "department": "Computer Science",
  "email": "john.doe@example.com",
  "password": "yourpassword"
}'
```

##### Response:

```json
{
  "message": "User registered successfully!"
}
```

### User Login

**POST /login**

Login an existing user.

```bash
curl -X POST https://eduvault.sabbir.co/api/login \
-H "Content-Type: application/json" \
-d '{
  "email": "john.doe@example.com",
  "password": "yourpassword"
}'
```

##### Response:

```json
{
  "message": "Login successful!"
}
```

### Create a Resource

**POST /resources**

Create a new resource. Requires user_id of the logged-in user.

```bash
curl -X POST https://eduvault.sabbir.co/api/resources \
-H "Content-Type: application/json" \
-d '{
  "title": "Resource Title",
  "description": "Resource Description",
  "category": "Category Name",
  "course_code": "CS101",
  "public_url": "https://resource-link.com",
  "user_id": 1
}'
```

##### Response:

```json
{
  "message": "Resource created successfully"
}
```

### Get All Resources

**GET /resources**

Retrieve a list of all available resources.

```bash
curl -X GET https://eduvault.sabbir.co/api/resources
```

##### Response:

```json
[
  {
    "id": 1,
    "title": "Resource Title",
    "description": "Resource Description",
    "category": "Category Name",
    "course_code": "CS101",
    "public_url": "https://resource-link.com"
  }
]
```

### Get Resource by ID

**GET /resources/{id}**

Retrieve a specific resource by its ID.

```bash
curl -X GET https://eduvault.sabbir.co/api/resources/1
```

##### Response:

```json
{
  "id": 1,
  "title": "Resource Title",
  "description": "Resource Description",
  "category": "Category Name",
  "course_code": "CS101",
  "public_url": "https://resource-link.com",
  "user_id": 1
}
```

### Update a Resource

**PUT /resources/{id}**

Update a resource's details.

```bash
curl -X PUT https://eduvault.sabbir.co/api/resources/1 \
-H "Content-Type: application/json" \
-d '{
  "title": "Updated Title",
  "description": "Updated Description",
  "category": "Updated Category",
  "course_code": "CS102",
  "public_url": "https://updated-resource-link.com"
}'
```

##### Response:

```json
{
  "message": "Resource updated successfully"
}
```

### Delete a Resource

**DELETE /resources/{id}**

Delete a resource by its ID.

```bash
curl -X DELETE https://eduvault.sabbir.co/api/resources/1
```

##### Response:

```json
{
  "message": "Resource deleted successfully"
}
```

### Save a Resource

**POST /save_resource**

Save a resource to the user's profile.

```bash
curl -X POST https://eduvault.sabbir.co/api/save_resource \
-H "Content-Type: application/json" \
-d '{
  "user_id": 1,
  "resource_id": 2
}'
```

##### Response:

```json
{
  "message": "Resource saved successfully."
}
```

### Unsave a Resource

**POST /unsave_resource**

Unsave a resource from the user's profile.

```bash
curl -X POST https://eduvault.sabbir.co/api/unsave_resource \
-H "Content-Type: application/json" \
-d '{
  "user_id": 1,
  "resource_id": 2
}'
```

##### Response:

```json
{
  "message": "Resource unsaved successfully."
}
```

### View User's Created Resources

**GET /user/{user_id}/created_resources**

View all resources created by a specific user.

```bash
curl -X GET https://eduvault.sabbir.co/api/user/1/created_resources
```

##### Response:

```json
[
  {
    "id": 1,
    "title": "Created Resource Title",
    "description": "Created Resource Description",
    "category": "Category Name",
    "course_code": "CS101",
    "public_url": "https://resource-link.com"
  }
]
```
