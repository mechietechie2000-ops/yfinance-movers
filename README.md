# This app is a wrapped on top of yahoo finance api, it pull the top movers from yfinance to make it lightweight
# Can be run on any platform but I'm running specifically on MacOS
# using Launchd daemon to run in the background

# To run the script manually 
```
cd yfinance-movers
uv run app.py
```

# Launchd Setup steps:

Find your uv path:
    which uv

Get the full path to your project folder:

``` 
cd yfinance-movers && pwd
``` 

### Open the plist I generated and replace the two placeholder paths (/path/to/uv and /path/to/yfinance-movers) with the real values from steps 1–2.
Copy it into the LaunchAgents folder and load it:

```
cp com.local.yfinance-movers.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.local.yfinance-movers.plist
```

That's it — it'll now start automatically on login and run silently in the background. 
# To check it's alive:

``` 
launchctl list | grep yfinance-movers
``` 

# To stop/unload it:
``` 
launchctl unload ~/Library/LaunchAgents/com.local.yfinance-movers.plist
``` 

# If something's wrong, check the logs:

```
cat /tmp/yfinance-movers.error.log
```

