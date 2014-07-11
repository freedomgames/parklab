Any files inside this directory will be served at /static/\<file\_name\>
For development purposes, you may use this to serve the
CSS, HTML and JavaScript you are writing and link them via their /static URI's.
In the templates, you can reference those locations with the
url\_for function, like so:

```html
<link rel=stylesheet type=text/css href="{{ url_for('static', filename='bootstrap.min.css') }}”>
```

This isn't something we'd want to depend upon for production, though.
It's silly to use Flask to serve static content,
so the final location for static assets like CSS, HTML and JavaScript
will be S3 and CloudFront.
You can put stuff in the 'static' directory and reference it like that
for development, but just make sure it's not too much of a pain to
change the URI's in the future.

Please don't fill this directory with any other static content.
Put things like images in S3 and use their S3 URI's --
no need to balloon the repo size with a bunch of images
that will be served elsewhere.

###### Note from Maia:

All files included in this directory are DEVELOPMENT only.
All files (CSS, JS, etc.) will be concatenated & minified,
pushed to Amazon, and served via CDN for production.
When we make a production version of this code,
all those changes will be implemented.

For the time being, this hosts all the source code. Go nuts! For now.