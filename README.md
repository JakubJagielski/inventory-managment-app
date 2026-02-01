To launch the software, run 

```sh
dockebuild -t atmio .
docker run -p 8000:8000 -v $(pwd)/data:/app/data atmio
```

Then open your browser and go to http://localhost:8000/components/