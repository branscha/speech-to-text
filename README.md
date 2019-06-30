# speech-to-text
A test of the Google speech to text API.

Contents

- app/: the micro service
- utils/: utility scripts to create test data (using text-to-speech)
  - Tools copied from the Google documentation for convenience.
- Dockerfile: containerize the application
  - A number of suggestions for base images, the slim-stretch is smaller than a standard ubuntu image. https://pythonspeed.com/articles/base-image-python-docker-images/

Notes

- Convert mp3 (from text-to-speech) to wav files (best result) using online converter: https://audio.online-convert.com/convert-to-wav



API design

- I opted for the POST verb in this simple API so that I could include a quick HTML GUI without  JavaScript and the cross-platform issues. Emphasis is on a working example, not on API nor GUI design.
- Sound file could be uploaded + converted to base 64. In that case GET, PUT also possible.  Some JavaScript code is necessary to construct a new request using the encoded data and talk to the REST API.
- I added the encoding parameter as an example on how the API could be further enhanced. The other parameters from the Google API  (eg language, frequency, ... ) could be added similarly.