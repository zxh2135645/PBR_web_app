from flask import Flask
app = Flask(__name__)

from flask import Flask
app = Flask(__name__)



def generate_html():
    from glob import glob
    starter_template = """
<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
    <title>AnatomicalPlotter</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:regular,bold,italic,thin,light,bolditalic,black,medium&amp;lang=en">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.cyan-light_blue.min.css">
    <link rel="stylesheet" href="https://rawgit.com/MEYVN-digital/mdl-selectfield/master/mdl-selectfield.min.css">
    <link rel="stylesheet" href="https://getmdl.io/templates/dashboard/styles.css"> 
    <script src="https://code.getmdl.io/1.3.0/material.min.js"></script>
    <script src="https://rawgit.com/MEYVN-digital/mdl-selectfield/master/mdl-selectfield.min.js"></script>
</head>

<body>

<main class="mdl-layout__content mdl-color--grey-100">
  <div class="mdl-grid demo-content">
     {body}
  </div>
</main>

</body>

</html>"""

    body_template = """

<div class="demo-charts mdl-card mdl-cell mdl-cell--12-col mdl-cell--4-col-tablet mdl-shadow--2dp">
  <figure class="mdl-card__media">
    <img src="/static/images/{pbr_name}/anatomical_image.png" alt="" />
  </figure>
  <div class="mdl-card__title">
    <h1 class="mdl-card__title-text">{pbr_name}</h1>
  </div>
  <div class="mdl-card__supporting-text">
  </div>
</div>"""

    all_image_folders = sorted(glob("static/images/ms*"))

    all_body = ""
    for image_folder in all_image_folders:
        # split the image_folder string so you extract the PBR name
        pbr_name = image_folder.split("/")[-1]
        # split the pbr name so we get the mse id
        mse = pbr_name.split("-")[1]
        # Use the body template to fill in the pbr_name and mse info:
        mse_body = body_template.format(mse=mse, pbr_name=pbr_name)
        # add the mse_body to all_body
        all_body += mse_body

    # Now fill body section of the starter_template:

    my_html = starter_template.format(body=all_body)
    return my_html

@app.route('/')
def hello_world():
    html = generate_html()
    return html

if __name__ == "__main__":
    app.run(port=1113)


