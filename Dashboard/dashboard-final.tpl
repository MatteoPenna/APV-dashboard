<!DOCTYPE html>
<html>
<script src="/js/jquery.min.js"></script>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>

.buttongo {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  margin: 4px 2px;
  cursor: pointer;
  font-size: 24px;
}

.buttonstop {
    background-color: #FF0000; /* Red */
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    margin: 4px 2px;
    cursor: pointer;
    font-size: 24px;}

.slidecontainer {
  width: 100%;
}

.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 25px;
  background: #d3d3d3;
  outline: none;
  opacity: 0.7;
  -webkit-transition: .2s;
  transition: opacity .2s;
}

.slider:hover {
  opacity: 1;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 25px;
  height: 25px;
  background: #4CAF50;
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 25px;
  height: 25px;
  background: #4CAF50;
  cursor: pointer;
}

/*creating code for two columns*/
* {
  box-sizing: border-box;
}

/* Create three unequal columns that floats next to each other */
.column {
  float: left;
  padding: 10px;
}

.left {
  width: 20%;
}

.right {
  width: 60%;
}

.middle {
  width: 20%;
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}

</style>

<style type="text/css">
  .tg  {border-collapse:collapse;border-spacing:0;border-color:#aaa;}
  .tg td{font-family:Arial, sans-serif;font-size:14px;padding:20px 20px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-top-width:1px;border-bottom-width:1px;border-color:#aaa;color:#333;background-color:#fff;}
  .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:20px 20px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-top-width:1px;border-bottom-width:1px;border-color:#aaa;color:#fff;background-color:#f38630;}
  .tg .tg-c3ow{border-color:inherit;text-align:center;vertical-align:top}
  .tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
  .tg .tg-0lax{text-align:left;vertical-align:top}
</style>

</head>
<body>

<h1> APV Control Dash</h1>
<p> Use the up and down arrow keys to control the speed of the APV 
and use the left and right arrow keys to change the steering of the APV.
</p>

<div class="row">
  <div class="column left" style="background-color:#bbb;">
    <h3>Setting of hyper parameters of the image processing algorithm</h3>

      <form action="hyper_params/image_processing" method = "POST" id='image_processing'>
        k_size (int)<br>
        <input type="text" name="k_size" value=""><br><br>
        k_h (int):<br>
        <input type="text" name="k_h" value=""><br><br>
        k_w (int)<br>
        <input type="text" name="k_w" value=""><br><br>
        lead_thresh (int):<br>
        <input type="text" name="lead_thresh" value=""><br><br>
        maxObjs (int)<br>
        <input type="text" name="maxObjs" value=""><br><br>
        thresh (int):<br>
        <input type="text" name="thresh" value=""><br><br>
        min_edge (int)<br>
        <input type="text" name="min_edge" value=""><br><br>
        max_edge (int):<br>
        <input type="text" name="max_edge" value=""><br><br>
        grid_rows (int)<br>
        <input type="text" name="grid_rows" value=""><br><br>
        grid_columns (int):<br>
        <input type="text" name="grid_columns" value=""><br><br>
        scaling_constant (int):<br>
        <input type="text" name="scaling_constant" value=""><br><br>
        scaling_power (int):<br>
        <input type="text" name="scaling_power" value=""><br><br>
        <input type="submit" value="Submit">
      </form>
  </div>
      
  <div class="column middle" style="background-color:#bbb;">
    <h3>Setting of hyper parameters of the decision making algorithm</h3>
    <form action="hyper_params/decision" method = "POST" id='decision'>
        dist_sensitivity (float):<br>
        <input type="text" name="dist_sensitivity" value=""><br><br>
        rpm_sensitivity (float):<br>
        <input type="text" name="rpm_sensitivity" value=""><br><br>
        catchup_sensitivity (float):<br>
        <input type="text" name="catchup_sensitivity" value=""><br><br>
        dist_set (float):<br>
        <input type="text" name="dist_set" value=""><br><br>
        ball_rad_m (float):<br>
        <input type="text" name="ball_rad_m" value=""><br><br>
        turn_sensitivity (float):<br>
        <input type="text" name="turn_sensitivity" value=""><br><br>
        turn_agression (float):<br>
        <input type="text" name="turn_agression" value=""><br><br>
        <input type="submit" value="Submit"><br><br>
    </form>

    <form action="hyper_params/image_capture" method="POST" id='resolution'>
      image_resolution (int):<br> 
      <input type="text" name="resolution" value=""><br><br>
      <input type="submit" value="Submit">
    </form>
    
    <br>
    
    <form action="killed" method = "POST">
      <button class="button buttonstop" id="kill">Kill</button>
    </form>
  </div>
  
  <div class="column right">
    <h2>Servo Slider</h2>
    <div class="slidecontainer">
      <input type="range" min="-45" max="45" value="0" class="slider" id="steering">
      <p>Turning Angle (servo angle in degrees): <span id="angle"></span></p>
    </div>

    <h2>Speed Control</h2>
    <div class="slidecontainer">
      <input type='range' min='-5' max='15' value='0' class='slider' id="speed">
      <p>Speed (in km/h): <span id="value"></span></p>
    </div>
    
    <br>
    
    <div>
      <table class="tg" style="undefined;table-layout: fixed; width: 549px">
      <colgroup>
      <col style="width: 263px">
      <col style="width: 286px">
      </colgroup>
        <tr>
        <th class="tg-c3ow">Sensor</th>
        <th class="tg-c3ow">Value</th>
        </tr>
        <tr>
        <td class="tg-0pky">RPM</td>
        <td class="tg-0pky" id="RPM"></td>
        </tr>
        <tr>
        <td class="tg-0pky">Ultrasonic Distance</td>
        <td class="tg-0pky" id="ultra_dist"></td>
        </tr>
        <tr>
        <td class="tg-0pky">Speed</td>
        <td class="tg-0pky" id="speed"></td>
        </tr>
        <tr>
        <td class="tg-0lax">Acceleration</td>
        <td class="tg-0lax" id="acceleration"></td>
        </tr>
        <tr>
        <td class="tg-0lax">Battery Temperature</td>
        <td class="tg-0lax" id="batteryTemp"></td>
        </tr>
        <tr>
        <td class="tg-0lax">Angular Velocity</td>
        <td class="tg-0lax" id="angularVelocity"></td>
        </tr>
        <tr>
        <td class="tg-0lax">Battery Output Voltage</td>
        <td class="tg-0lax" id="batteryVoltage"></td>
        </tr>
      </table>
    </div>

  </div>
</div>


</body>
</html>

<script>
//variables for the speed and angle sliders
var slider_steering = document.getElementById("steering");
var slider_speed = document.getElementById("speed")
var output_steering = document.getElementById("angle");
var output_speed = document.getElementById("value");

//updating variables for speed and angle sliders
var current_angle = parseInt(slider_steering.value);
var current_speed = parseInt(slider_speed.value);

//image_processing parameter variables
var image_processing_obj = {
  k_size : document.getElementsByName('k_size'),
  k_h : document.getElementsByName('k_h'),
  k_w : document.getElementsByName('k_w'),
  lead_thresh : document.getElementsByName('lead_thresh'),
  maxObjs : document.getElementsByName('maxObjs'),
  thresh : document.getElementsByName('thresh'),
  min_edge : document.getElementsByName('min_edge'),
  max_edge : document.getElementsByName('max_edge'),
  grid_rows : document.getElementsByName('grid_rows'),
  grid_columns : document.getElementsByName('grid_columns'),
  scaling_constant : document.getElementsByName('scaling_constant'),
  scaling_power : document.getElementsByName('scaling_power')
}; 
var image_processing_data = JSON.stringify(image_processing_obj); 

//decision_making parameter variables
var decision_params_obj = {
  dist_sensitivity : document.getElementsByName('dist_sensitivity'),
  rpm_sensitivity : document.getElementsByName('rpm_sensitivity'),
  catchup_sensitivity : document.getElementsByName('catchup_sensitivity'),
  dist_set : document.getElementsByName('dist_set'),
  ball_rad_m : document.getElementsByName('ball_rad_m'),
  turn_sensitivity : document.getElementsByName('turn_sensitivity'),
  turn_agression : document.getElementsByName('turn_aggression')
}

var resolution = JSON.stringify(resolution : document.getElementsByName('resolution')) 

/*this code is for submitting requests to the webserver in json format
for easy readout on the web server side*/
$('#image_processing').click(function () {
    $.ajax({
      type: "POST",
      url: 'hyper_params/image_processing',
      data: image_processing_params,
      success: function () {
        console.log(data)
      },
      dataType: 'json'
      });
});

$('#decision').click(function () {
    $.ajax({
      type: "POST",
      url: 'hyper_params/decision',
      data: decision_params,
      success: function () {
        console.log(data)
      },
      dataType: 'json'
      });
});

$('#resolution').click(function () {
    $.ajax({
      type: "POST",
      url: 'hyper_params/image_capture',
      data: resolution,
      success: function () {
        console.log(data)
      },
      dataType: 'json'
      });
});

//This code is for updating the data table
$(document).ready(function () {
  
  var auto_refresh = setInterval(function () {
    $.ajax({
      url: "get_data",
      type: "GET",
      success: function (data) {
        console.log(data);
        var values = data;
        $("#RPM").html(values.rpm);
        $("#ultra_dist").html(values.ultraDist);
        $("#speed").html(values.speed);
        $("#acceleration").html(values.acceleration);
        $("#batteryTemp").html(values.batteryTemp);
        $("#batteryVoltage").html(values.batteryVoltage);
        $("#angularVelocity").html(values.angularVelocity);
      },
      dataType: 'json'
    });
  }, 100)
})  

//add minimum values if statements
document.onkeydown = function(e) {
  
  switch (e.keyCode) {
    case 37:
      //left;
      current_angle -= 2;
      slider_steering.value = current_angle;
      console.log(current_angle);
      break;
    case 38:
      //up;
      current_speed += 0.5;
      slider_speed.value = current_speed;
      console.log(current_speed);
      break;
    case 39:
      //right;
      current_angle += 2;
      slider_steering.value = current_angle;
      console.log(current_angle);
      break;
    case 40:
      //down;
      current_speed -= 0.5;
      slider_speed.value = current_speed;
      console.log(current_speed);
      break;
      }
      
      output_steering.innerHTML = current_angle;
      output_speed.innerHTML = current_speed;

      $.post("speed_and_angle", {
        speed: String(current_speed),
        angle: String(current_angle)
      })
      
};


/*
      slider_steering.oninput = function(){
      output_steering.innerHTML = this.value;
      }

      slider_speed.oninput = function() {
      output_speed.innerHTML = this.value;
      }
*/      

/*
$.post('localhost:8080/speed_and_angle', {
    speed : String(slider_speed)
    angle : String(slider_steering)
    })
*/

</script> 
