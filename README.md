
# Top Infinity

Quantum Acoustics Chorus's website - created as a high school project in my last year. Uses Flask, Prisma and TailwindCSS to make a full stack app that renders a beautiful front page that can also be changed through the backend side of the site.

## Lessons Learned

Using what I had previously learnt about user handling and outdated or lacking technologies for a complex full0stack app, I stuck to Python Flask but adding TailwindCSS for a smoother frontend development experience and Prisma to connect to the database using more standard solutions that are used in the industry.

Once I started creating this website, I came to the limit of what Python Flask had to offer, having to resort to pure Javascript and JQuery for a lot of frontend functions. From this, I learnt the limitations of Flask and decided to transition this app into a React app (in collaboration with a friend), which can be found [here](https://github.com/baritone-designs/harmony-waitaha-website).


## Initialisation Commands

To deploy this project run
```console
python -m venv .venv
npm install
npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css
prisma db push
pip install requirements.txt
py app.py
```

## Authors

- [@JoranQuack (me)](https://github.com/JoranQuack)

