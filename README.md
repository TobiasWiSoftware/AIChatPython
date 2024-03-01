# Python AI Chat App - Dokumentation

## 1. Used features

### Framework: React, Flask

### Datasource: ChatGPT Api

## 2. Setup

### 2.1 Frontend

- **Command PS:**           `cd client`

- **Command PS:**           `npx create-react-app .`

- **Command PS:**           `npm start`

- **Command PS:**           `npm install bootstrap axois react-router-dom`

- **Command PS:**           `cd src`

- **Command PS:**           `New-Item pages -ItemType Directory`

- **Command PS:**           `cd pages`

- **Command PS:**           `New-Item Chat.jsx`

- **Command PS:**           `New-Item Upload.jsx`

- **Command PS:**           `cd ..`

- **Command PS:**           `New-Item components -ItemType Directory`

- **Command PS:**           `cd components`

- **Command PS:**           `New-Item Navbar.jsx`

- **Command PS:**           `cd..`

- **Command PS:**           `add "proxy": "http://localhost:5000" for server connection`






### 2.2 Backend

- **Command PS:**           `cd server`

- **Command PS:**           `pip install virtualenv`

- **Command PS:**           `virtualenv <name>`

- **Command PS:**           `powershell -ExecutionPolicy Bypass`

- **Command PS:**           `<name>\Scripts\activate`

- **Command PS:**           `pip install flask flask-cors`

- **Command PS:**           `New-Item Server.py -ItemType File`

- **Command PS:**           `python Server.py`

- **Command PS:**           `pip freeze > requirements.txt` - saving the components





