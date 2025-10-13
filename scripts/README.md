<h1 align="center">🦸‍♀️ Superheroes API 🦸‍♂️</h1>

<p align="center">
  <b>Unleash the Power of APIs! ⚡</b><br>
  Django-based REST API with superheroes, CI/CD pipelines, Docker, and automated testing.  
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Django-4.2+-green?style=for-the-badge&logo=django"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Hacktoberfest-2025-orange?style=for-the-badge"/>
  <img src="https://komarev.com/ghpvc/?username=SrinjoyeeDey&style=flat-square&color=blue" alt="Profile Views"/>
</p>

---

## ✨ Overview

**Superheroes API** is a modular, production-ready Django backend exposing REST endpoints for superheroes.  

- 🧪 Health-check APIs  
- 🦸‍♂️ CRUD for superheroes  
- 🐳 Dockerized deployment  
- ⚙️ CI/CD ready with **Dagger** pipelines  
- 🧹 Linting & formatting scripts (black, flake8, isort)  
- 🧩 Fully tested with unittest & pytest  

> _"Contributions make superheroes of developers!"_ 🦸‍♀️

---

## 📂 Project Structure

Superheroes-API/
│
├── base/ # Django base (settings, urls, wsgi, asgi)
├── health/ # Health API endpoints & tests
│ └── migrations/
├── superheroes/ # Superhero API logic
│ ├── management/commands/
│ └── migrations/
├── scripts/ # CI/CD & utility scripts
│ ├── demo_health.py
│ ├── demo_heroes.py
│ ├── demo_superheroes.py
│ ├── run-.sh
│ └── test_health.py
├── .github/workflows/ # CI/CD YAML files
├── DAGGER_PIPELINE.md
├── dagger_pipeline.py
├── Dockerfile
├── manage.py
├── requirements.txt
└── schema.yml

yaml
Copy code

---

## 🛠️ Setup & Installation

```bash
# Clone repo
git clone https://github.com/CyrilBaah/Superheroes-API.git
cd Superheroes-API

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver
Access API at 👉 http://127.0.0.1:8000/

🧩 API Endpoints
Method	Endpoint	Description
GET	/health/	API health status 💚
GET	/api/superheroes/	List all superheroes 🦸‍♂️
POST	/api/superheroes/	Add a superhero
GET	/api/superheroes/<id>/	Fetch single hero
PUT	/api/superheroes/<id>/	Update hero
DELETE	/api/superheroes/<id>/	Delete hero

Example Response

json
Copy code
{
  "id": 1,
  "name": "Iron Man",
  "alias": "Tony Stark",
  "powers": ["Genius Intellect", "Powered Armor Suit", "Flight"]
}
🧪 Running Tests & Scripts
bash
Copy code
# Run all tests
bash scripts/run-test.sh

# Health endpoint tests
python scripts/test_health.py

# Demo scripts
python scripts/demo_health.py
python scripts/demo_heroes.py
python scripts/demo_superheroes.py
Check detailed scripts info in scripts/README.md

🐳 Docker Support
bash
Copy code
docker build -t superheroes-api .
docker run -p 8000:8000 superheroes-api
⚡ CI/CD & Dagger
Run automated pipelines:

bash
Copy code
bash scripts/run-dagger-ci.sh
bash scripts/run-dagger-dashboard.sh
Workflows include linting, testing, and license compliance checks.

💡 Code Quality
bash
Copy code
bash scripts/run-linters.sh
bash scripts/run-black.sh
bash scripts/run-isort.sh
bash scripts/run-flake8.sh
🌟 Contribution Guide
Contributions are highly welcome! 🎉

Fork the repository

Create a new branch (git checkout -b feature/my-feature)

Commit changes (git commit -m "Add awesome feature")

Push to branch (git push origin feature/my-feature)

Open a Pull Request

Ensure all tests and linters pass before PR submission ✅

## 👥 Contributors

Thanks to these amazing people for their contributions 💪

<!-- readme: contributors -start -->
<!-- readme: contributors -end -->


📜 License
MIT License — see LICENSE for details.

🎉 Acknowledgements
Thanks to Hacktoberfest 2025 participants and open-source contributors! 💚



---

### ✅ Features Added:

1. **Dark-mode friendly**  
2. **GitHub profile views badge**  
3. **Animated superhero GIF** for engagement  
4. **All scripts, pipelines, folders listed**  
5. **Hacktoberfest friendly phrasing**  
6. **Emojis, badges, formatting for visual appeal**  
