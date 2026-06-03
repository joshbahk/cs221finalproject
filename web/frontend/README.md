# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

## Running the Project

To run the project locally, open two terminal windows from the project root directory.

### Backend

Start the FastAPI backend server:

```bash
uvicorn web.backend.server:app --reload
```

### Frontend

In a second terminal, start the React frontend:

```bash
cd web/frontend
npm install
npm run dev
```

> Note: `npm install` is only required the first time you set up the project.

### Accessing the Application

Once both servers are running, open the URL displayed by Vite in your browser (typically `http://localhost:5173`).

The frontend will communicate with the FastAPI backend running locally.
