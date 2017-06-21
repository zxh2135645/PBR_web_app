from flask import Flask, redirect
from glob import glob
from flask import request


app = Flask(__name__)

@app.route('/')
def hello_world():
    all_image_folders = sorted(glob("static/images/ms*"))

    return generate_html(all_image_folders)

def generate_html(all_image_folders, title="All Images"):
    from glob import glob
    starter_template = """
<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
    <title>AnatomicalPlotter</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.1.1.slim.min.js" integrity="sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css" type="text/css" >

</head>


<body>

<nav class="navbar sticky-top navbar-toggleable-md navbar-light bg-faded">
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
    <a class="navbar-brand" href="#">PBRain Labeller</a>
    <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
      <li class="nav-item active">
        <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">About</a>
      </li>    </ul>
    <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="text" placeholder="Search">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form>
  </div>
</nav>

<div class="" style="margin:20px;">

  <div class="form-check form-check-inline">
   <form id="myForm" class="form-group" action="/saveForm">
<div class="jumbotron" style="margin-top:10px;">
  <h1 class="display-3">{title}</h1>
  <p class="lead">Identify image modality and body part</p>
  <hr class="my-4">
  <p>Choose between T1 and T2 image modality, and brain or spinal cord</p>
  <p class="lead">
    <button class="btn btn-primary btn-lg" type="submit">Save</button>
  </p>
</div>

<div class="row">
     {body}
</div>
   </form>
  </div>
</div>

</body>

</html>"""

   
    body_template = """
<div class="col-xs">
    <div class="card mb-3">
      <img class="card-img-top" src="/static/images/{pbr_name}/anatomical_image.png"  alt="Card image cap">
      <div class="card-block">
        <h4 class="card-title">{pbr_name}</h4>
        <p class="card-text">
        <div class="form-check form-check-inline">
          <label class="form-check-label">
            <input class="form-check-input" type="radio" name="{pbr_name}___type" id="inlineRadio1-{idx}" value="brain"> Brain
          </label>
        </div>
        <div class="form-check form-check-inline">
          <label class="form-check-label">
            <input class="form-check-input" type="radio" name="{pbr_name}___type" id="inlineRadio2-{idx}" value="spine"> Spine
          </label>
        </div>

  <div class="form-group">
    <label for="exampleSelect1-{idx}">Choose Modality</label>
    <select class="form-control" id="exampleSelect1i{idx}" name="{pbr_name}___modality">
      <option>Ignore</option>
      <option>T1</option>
      <option>T2</option>
      <option>FLAIR</option>
      <option>Diffusion</option>
    </select>
  </div>

       </p>
      </div>
    </div>

</div>
      """

    all_body = ""
    N = len(all_image_folders)
    for idx, image_folder in enumerate(all_image_folders):
        # split the image_folder string so you extract the PBR name
        pbr_name = image_folder.split("/")[-1]
        # split the pbr name so we get the mse id
        mse = pbr_name.split("-")[1]
        # Use the body template to fill in the pbr_name and mse info:
        mse_body = body_template.format(mse=mse, pbr_name=pbr_name, idx=idx)
        # add the mse_body to all_body
        all_body += mse_body

    # Now fill body section of the starter_template:

    my_html = starter_template.format(body=all_body, title=title)
    return my_html



@app.route('/msid/<msid>')
def show_msid_images(msid):
    # show the user profile for that user
    msid_images = sorted(glob("static/images/{}-*".format(msid)))
    return generate_html(msid_images, msid)

@app.route('/saveForm')
def save_form():
    print(request.args)
    # show the user profile for that user
    return redirect("/")

from flask import Flask, redirect, jsonify

@app.route("/getData/<globStr>", methods=['GET'])
def get_data(globStr):
    image_folders = sorted(glob("static/images/{}*/anatomical_image.png".format(globStr)))
    output_urls = ["/"+s for s in image_folders] #static is in root
    output_data = [{"url": url, "type": None, "part": None,
                    "pbr_name": image_folders[i].split("/")[-2]} for i, url in enumerate(output_urls)]
    return jsonify(output_data)

import json
@app.route("/saveData/", methods=['POST'])
def save_data():
    data = json.loads(request.get_data().decode('utf-8'))
    print(data)
    #do something with the data here -- save it to a file? 
    return "Success! This message is from the server"


if __name__ == "__main__":
    app.run(port=1113)
