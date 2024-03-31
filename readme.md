## Use Raspberry PI Pico for Timetracking

Blogpost: https://madflex.de/use-pico-track-time

### Setup

Copy app/.secrets.template to app/.secrets and fill in your configuration from <https://toggl.com>.

Install the requirements:
```
pip install -r requirements.txt
```

### Running the Flask server
```
flask --app app.main run
```
