# Teaching Assistant AI

An AI-powered teaching assistant that helps educators generate lecture plans and receive feedback on their teaching. This project was developed during the Sundai Hackathon 2024.

## About

This project was created as part of the Sundai Hackathon 2024, where we aimed to develop innovative solutions for education using AI technology. The Teaching Assistant AI helps educators improve their teaching methods through AI-powered feedback and lesson planning.

## Features

- Generate detailed lecture plans
- Receive comprehensive teaching feedback
- Analyze classroom interactions
- Track teaching metrics
- Dark theme interface

## Setup

1. Clone this repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running Locally

To run the application locally:
```bash
streamlit run app.py
```

## Deployment Options

### 1. Streamlit Cloud (Recommended)

1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and main file (app.py)
6. Add your environment variables (OPENAI_API_KEY)
7. Click "Deploy"

### 2. Heroku

1. Create a `Procfile`:
```
web: streamlit run app.py
```

2. Create a `runtime.txt`:
```
python-3.11.9
```

3. Deploy to Heroku:
```bash
heroku create your-app-name
git push heroku main
```

4. Set environment variables:
```bash
heroku config:set OPENAI_API_KEY=your_api_key_here
```

### 3. AWS Elastic Beanstalk

1. Create a `requirements.txt` (already included)
2. Create a `.ebextensions/python.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app.py
```

3. Deploy using AWS CLI or console

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Developed during Sundai Hackathon 2024
- Special thanks to all the mentors and organizers who supported this project
