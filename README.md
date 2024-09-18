# BioverseApplication

This is a full-stack web application where users can answer questionnaires and administrators can view user answers. The front end is built with **Next.js** and **Material UI**, while the back end is powered by **FastAPI** and **PostgreSQL**.

## Table of Contents

- [Frontend](#frontend)
  - [Technologies](#frontend-technologies)
  - [Installation and Running](#frontend-installation-and-running)
- [Backend](#backend)
  - [Technologies](#backend-technologies)
  - [Installation and Running](#backend-installation-and-running)
- [Docker Setup](#docker-setup)

---

## Frontend

### Frontend Technologies

- **Next.js**: A React framework for server-side rendering and static site generation.
- **Material UI**: A popular React UI framework for building modern, responsive UIs.
- **TypeScript**: Adds type safety and improved tooling for JavaScript.
- **Vercel**: The frontend is deployed on Vercel.

### Frontend Installation and Running

1. Clone the repository:
2. Install dependencies:

   \`\`\`bash
   npm install
   \`\`\`
3. Run the development server:

   \`\`\`bash
   npm run dev
   \`\`\`
4. Access the frontend at \`http://localhost:3000\`.
5. Build for production:

   \`\`\`bash
   npm run build
   \`\`\`
6. Run the production server:

   \`\`\`bash
   npm start
   \`\`\`

### Deployed Application

The frontend is deployed on **Vercel** and can be accessed at:
[[[https://your-vercel-url.vercel.app](https://your-vercel-url.vercel.app)
](https://bioverse-frontend-lime.vercel.app/)](https://bioverse-frontend-lime.vercel.app/)
------------------------------------------------------------------------------------------

## Backend

### Backend Technologies

- **FastAPI**: A modern, fast web framework for building APIs with Python 3.7+.
- **PostgreSQL**: A powerful, open-source relational database.
- **Docker**: Used for containerization of both the API and PostgreSQL.
- **Uvicorn**: ASGI server used to serve FastAPI.
- **SQLAlchemy**: ORM for database interaction.

### Backend Installation and Running

1. Clone the repository:
2. run init.sh script
3. Create and set up the PostgreSQL database:

   - Start PostgreSQL service.
   - Create a new database and user as outlined in the steps above.
4. The API will be available at \`http://localhost:8000\`.

---

### Deployed Backend

The backend is deployed on an EC2 instance. You can access the API at:
\`www.bioverseapp.com`

There is an admin user and test user added to the db but additional users can be created.

admin

username: admin, password: admin

test user

username: test, password: test

## Docker Setup

The project uses **Docker Compose** to manage back-end services.

1. Make sure Docker is installed and running on your machine.
2. running the init script will create backend docker containers

---

## License

This project is licensed under the MIT License. See the \`LICENSE\` file for details.

---
