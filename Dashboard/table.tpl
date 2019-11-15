<!DOCTYPE html>
<html>
<head>
<!--    <meta http-equiv="refresh" content="0.5; url=http://localhost:8080/sensordash"> -->
</head>
<script src="/js/jquery.min.js"></script>
<body>
<style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:0;border-color:#aaa;}
    .tg td{font-family:Arial, sans-serif;font-size:14px;padding:20px 20px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-top-width:1px;border-bottom-width:1px;border-color:#aaa;color:#333;background-color:#fff;}
    .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:20px 20px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-top-width:1px;border-bottom-width:1px;border-color:#aaa;color:#fff;background-color:#f38630;}
    .tg .tg-c3ow{border-color:inherit;text-align:center;vertical-align:top}
    .tg .tg-0pky{border-color:inherit;text-align:left;vertical-align:top}
    .tg .tg-0lax{text-align:left;vertical-align:top}
    </style>
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
    
<script>

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

/*
    $.get("data", function (data) {
        console.log(data);
        var values = JSON.parse(data);
        $("#RPM").html(values.rpm)
    })
*/


</script>

</body>
</html>

