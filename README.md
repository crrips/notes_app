# Notes App

This application allows you to create, edit, and delete notes and summarize them using AI. It uses the Gemini API to summarize the notes. There is also an analytics page that shows statistics about the notes.

![Home page](/images/home.png)

## 🚀 Launch

Firstly, create an .env file in the backend directory and set the following values:
```
GEMINI_API_KEY =
```

To start the app using Docker and docker-compose, run:
```
docker-compose up --build
```

![Analytics page](/images/analytics.png)

## 🛠️ Development

* Backend: FastAPI
* Frontend: Vue.js
* Database: PostgreSQL
* Deployment: Docker
* AI: Gemini API
* Analytics: Pandas and Numpy

![Summarize](/images/summarize.png)

## 🧪 Testing

‼️ TESTS SHOULD RUN ONLY INSIDE THE CONTAINER ‼️

After starting the application, you need to know the container ID of the backend container. You can find it by running the following command:
```
docker ps
```

Then, you can run the following command to enter the container:
```
docker exec -it <container_id> sh
```

To run tests, you can run the following command:
```
pytest app/tests.py
```

## 📩 Feedback

Feel free to contact me if you have any suggestions or issues.
