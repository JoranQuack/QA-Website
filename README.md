# QA-Website
 Quantum Acoustics Chorus's website

python -m venv .venv
npm install
npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css
prisma db push
pip install requirements.txt
py app.py