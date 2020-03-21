# sic-feedback
sic-feedback is a tool for adding URLs to shouldiclick database.

For using this tool you need to have an API key. If you do not have it contact us.

#### Usage:
* Submit "www.google.com" as normal website: 
    * ```python sic-feedback.py -u 'www.google.com' -l 0```

* Submit "www.google.com" as normal website wit public scan.: 
    * ```python sic-feedback.py -u 'www.google.com' -l 0 -p```
    
* Submit "www.phishing-website.com" as phishing website.
    * ```python sic-feedback.py -u 'www.phishing-website.com' -l 2```
