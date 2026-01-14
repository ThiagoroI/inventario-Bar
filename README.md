Bar Inventory Management System
A full-stack bar inventory management system designed to manage products, stock levels, and user access efficiently. This project is built using Django and React, following clean software engineering principles and a layered (N-tier) architecture.
The system exposes a RESTful API, implements secure authentication and authorization using JWT, and uses a MySQL database optimized through ORM-based data modeling.
________________________________________
Features
•	Product and inventory management
•	Stock tracking and updates
•	Role-based access control (admin / staff)
•	JWT-based authentication and authorization
•	RESTful API for frontend-backend communication
•	Layered (N-tier) architecture
•	ORM-based database modeling and optimization
________________________________________
Tech Stack
Backend
•	Django
•	Django REST Framework
•	JWT Authentication
Frontend
•	React
•	HTML
•	CSS
Database
•	MySQL
________________________________________
Architecture
The project follows a layered (N-tier) architecture, which separates responsibilities into distinct layers:
•	Presentation Layer: React frontend responsible for the user interface
•	Application Layer: RESTful API handling requests and responses
•	Business Logic Layer: Core application rules and processes
•	Data Access Layer: ORM-based interaction with the MySQL database
This approach improves maintainability, scalability, and testability.
________________________________________
API Overview
The backend exposes RESTful endpoints for managing authentication, users, and inventory resources. Protected endpoints require a valid JWT token and enforce access based on user roles.
________________________________________
Authentication & Authorization
Authentication is implemented using JSON Web Tokens (JWT).
•	Users authenticate with credentials and receive an access token
•	Protected endpoints require a valid token
•	Authorization is role-based (e.g., admin, staff)
This ensures secure access control throughout the application.
________________________________________
Installation & Setup
Prerequisites
•	Python 3.x
•	Node.js and npm
•	MySQL
Backend Setup
1.	Clone the repository
2.	Create and activate a virtual environment
3.	Install Python dependencies
4.	Configure environment variables
5.	Run database migrations
6.	Start the Django development server
Frontend Setup
1.	Navigate to the frontend directory
2.	Install dependencies
3.	Start the React development server
________________________________________
Environment Variables
The backend requires environment variables for database configuration, secret keys, and JWT settings. These should be defined in a local environment file and excluded from version control.
________________________________________
Future Improvements
•	Automated unit and integration testing
•	Reporting and analytics dashboard
•	Improved UI/UX design
•	CI/CD pipeline integration
•	Deployment configuration
________________________________________
Author
Developed by Santiago Nonsoque
________________________________________
License
This project is for educational and portfolio purposes.
