To launch the software, run 

```sh
docker build -t inventory_manager .
docker run -p 8000:8000 -v $(pwd)/data:/app/data inventory_manager
```

Then open your browser and go to http://localhost:8000/components/



To run tests, do

```sh
poetry install --no-root
PYTHONPATH=src poetry run pytest tests/
```