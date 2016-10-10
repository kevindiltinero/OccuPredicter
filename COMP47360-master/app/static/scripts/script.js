// This function selects the appropriately coloured image for each room depending on the occupancies passed in as parameters.
//
function chooseImage(val1, val2, val3, val4, val5, val6) {
        var occ = [val1, val2, val3, val4, val5, val6];
        var rooms = ["B004", "B002", "B003", "B106", "B108", "B109"];
        var corresponse = ['05', '04', '05', '13', '11', '12'];

        for (var i =0; i < occ.length; i++){
                if (occ[i] == 0){
                    document.getElementById(rooms[i]).src = "../static/images/Map2_"+corresponse[i]+".jpg";
                } else if (occ[i] == 25){
                    document.getElementById(rooms[i]).src = "../static/images/Map3_"+corresponse[i]+".jpg";
                } else if (occ[i] == 50){
                    document.getElementById(rooms[i]).src = "../static/images/Map4_"+corresponse[i]+".jpg";
                } else if (occ[i] == 75) {
                    document.getElementById(rooms[i]).src = "../static/images/Map5_"+corresponse[i]+".jpg";
                } else {
                    document.getElementById(rooms[i]).src = "../static/images/Map06_"+corresponse[i]+".jpg";
            }
        }
}

/* Functions to toggle divs on the "data" page */
/* Simplay toggles the displays of various divs based on the results */

function showWifi() {
        document.getElementById("wifi-upload").style.display = "block";
        document.getElementById("ground-upload").style.display = "none";
        document.getElementById("upload-select").style.display = "none";
        document.getElementById("wifi-fail").style.display = "none";
        document.getElementById("wifi-success").style.display = "none";
}

function showGround() {
        document.getElementById("wifi-upload").style.display = "none";
        document.getElementById("ground-upload").style.display = "block";
        document.getElementById("upload-select").style.display = "none";
        document.getElementById("ground-fail").style.display = "none";
        document.getElementById("ground-success").style.display = "none";
}

function process_results(success, type) {
        if(success == "true") {
                if(type == "wifi") {
                        document.getElementById("wifi-upload").style.display = "block";
                        document.getElementById("wifi-success").style.display = "block";
                        document.getElementById("upload-select").style.display = "none";
                }
                else {
                        document.getElementById("ground-upload").style.display = "block";
                        document.getElementById("ground-success").style.display = "block";
                        document.getElementById("upload-select").style.display = "none";
                }
        }
        else {
                if(type == "wifi") {
                        document.getElementById("wifi-upload").style.display = "block";
                        document.getElementById("wifi-fail").style.display = "block";
                        document.getElementById("upload-select").style.display = "none";
                }
                else {
                        document.getElementById("ground-upload").style.display = "block";
                        document.getElementById("ground-fail").style.display = "block";
                        document.getElementById("upload-select").style.display = "none";
                }

        }
}
