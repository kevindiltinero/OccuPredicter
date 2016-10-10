////////////////////   GET ALL THE RESULTS FROM FLASK  events predictions, hour, day etc         ///////////////////////
        var day = '{{ day }}';
        var hour = '{{ hour }}';
        var room = '{{ room }}';
        var extra = '{{ extra }}';
        var predictions = '{{ values[1] }}';
        var cspred = ['{{ values[0][0] }}', '{{ values[0][1] }}', '{{ values[0][2] }}', '{{ values[0][3] }}', '{{ values[0][4] }}', '{{ values[0][5] }}'];
        var hubpred = ['{{ values[1][0] }}', '{{ values[1][1] }}', '{{ values[1][2] }}', '{{ values[1][3] }}', '{{ values[1][4] }}', '{{ values[1][5] }}', '{{ values[1][6] }}', '{{ values[1][7] }}', '{{ values[1][8] }}', '{{ values[1][9] }}', '{{ values[1][10] }}', '{{ values[1][11] }}'];
        var answer = '{{ events }}';

        // Using the dom here to write to elements values to check if flask is sending them over.
        document.getElementById('checking').innerHTML = answer;
{#        document.getElementById('checking').innerHTML = hubpred;#}
{#        document.getElementById('checking2').innerHTML = roomchange;#}
{#        document.getElementById(roomchange).style.visibility = 'visible';#}


//////////////////////////////////   FUNCTION TO PLOT THE ICONS BASED ON EVENTS TABLE         //////////////////////////
        //This is doing this in a basic sense but I know exactly how I will get it working
        function iconsChange(answer) {
            var x = document.getElementsByClassName("present");
            if (answer == 'y') {
                var i;
                for (i = 0; i < x.length; i++) {
                    x[i].style.visibility = "visible";
                }
            } else if (answer == 'n') {
                for (i = 0; i < x.length; i++) {
                    x[i].style.visibility = "hidden";
        }
            }
        }
        
// Calling the function
        iconsChange(answer);


//////////////////////////////////  JQUERY FUNCTION FADE ICONS IN AND FADE OUT         //////////////////////////
                setInterval(function(){
            $(".present").fadeOut(function() {
                $(this).attr("src","{{ url_for('static', filename='images/career.png') }}").fadeIn().delay(500).fadeOut(function(){
                    $(this).attr("src", "{{ url_for('static', filename='images/career.png') }}").fadeIn().delay(500);
                });
             }
            );
        }, 400);


//////////////////////////////////////          POP UP WINDOW FUNCTION         ////////////////////////////////////////
        // Get the modal
        var modal = document.getElementById('myModal');
        // Get the image and insert it inside the modal - use its "alt" text as a caption
        var img = document.getElementById('myImg');
        var modalImg = document.getElementById("img01");
        var captionText = document.getElementById("caption");
        function doThis(){
            if (!e) var e = window.event;
            e.cancelBubble = true;
            if (e.stopPropagation) e.stopPropagation();
            modal.style.display = "block";
            modalImg.src = '{{ url_for('static', filename='images/meet.jpg') }}';
            modalImg.alt = this.alt;
            captionText.innerHTML = 'Allow miles wound place the leave had. To sitting subject no improve studied limited. ' +
                    'Ye indulgence unreserved connection alteration appearance my an astonished. Up as seen sent make he they ' +
                    'of. Her raising and himself pasture believe females. Fancy she stuff after aware merit small his. Charmed ' +
                    'esteems luckily age out.';
        }
        // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("close")[0];
        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
            modal.style.display = "none";
        }



////////////////////////////          CHANGES WHICH MAP IS DISPLAYED         ////////////////////////////////////////
        // Changes which building map is displayed based on the home page form

        function changeRoom(){
            if (room == 'Computer Science'){
                document.getElementById('map').style.display = "inline-block";
                document.getElementById('maphub').style.display = "none";
                csPlot(cspred);
            } else if (room == 'Science Hub'){
                document.getElementById('maphub').style.display = "inline-block";
                document.getElementById('map').style.display = "none";
                hubPlot(hubpred);
            } else {
                void(0);
            }
        }
        changeRoom();



////////////////////////////       PROGRAM TO PLOT THE COLORS          ////////////////////////////////////////

        // This plots the colors of the CS.
        function csPlot(item) {
            results = item;
            var slices = ['slicethree', 'slicefour', 'slicefive', 'slicenine', 'sliceten', 'sliceseleven'];
            var corresponse = ['03', '04', '05', '09', '10', '11'];
            for (var i =0; i < results.length; i++){
                if (results[i] == 0){
                    document.getElementById(slices[i]).style.background = "url(../static/images/CS1_"+corresponse[i]+".png)";
                } else if (results[i] == 1){
                    document.getElementById(slices[i]).style.background = "url(../static/images/CS2_"+corresponse[i]+".png)";
                } else if (results[i] == 2){
                    document.getElementById(slices[i]).style.background = "url(../static/images/CS3_"+corresponse[i]+".png)";
                } else if (results[i] == 3) {
                    document.getElementById(slices[i]).style.background = "url(../static/images/CS4_"+corresponse[i]+".png)";
                } else if (results[i] == 4) {
                    document.getElementById(slices[i]).style.background = "url(../static/images/CS5_"+corresponse[i]+".png)";
                } else {
                    document.getElementById(slices[i]).style.background = "url(../static/images/CS6_"+corresponse[i]+".png)";
                }
            }

        }

        //This changes the hub colors.
        function hubPlot(hubpred){
            var hresults = hubpred;
            //PROGRAM TO CHANGE THE MAP BASED ON THE RESULTS
            var hslices = ['hslice3', 'hslice4', 'hslice8', 'hslice9', 'hslice10', 'hslice12', 'hslice13', 'hslice17', 'hslice18', 'hslice19', 'hslice21', 'hslice22'];
            var hcorresponse = ['06', '07', '11', '12', '13', '15', '16', '20', '21', '22', '24', '25'];
            for (var i =0; i < hresults.length; i++){
                if (hresults[i] == 0){
                    document.getElementById(hslices[i]).style.background = "url(../static/images/Hub1_"+hcorresponse[i]+".png)";
                } else if (hresults[i] == 1){
                    document.getElementById(hslices[i]).style.background = "url(../static/images/Hub2_"+hcorresponse[i]+".png)";
                } else if (hresults[i] == 2){
                    document.getElementById(hslices[i]).style.background = "url(../static/images/Hub3_"+hcorresponse[i]+".png)";
                } else if (hresults[i] == 3) {
                    document.getElementById(hslices[i]).style.background = "url(../static/images/Hub4_"+hcorresponse[i]+".png)";
                } else if (hresults[i] == 4) {
                    document.getElementById(hslices[i]).style.background = "url(../static/images/Hub5_"+hcorresponse[i]+".png)";
                } else {
                    document.getElementById(hslices[i]).style.background = "url(../static/images/Hub5_"+hcorresponse[i]+".png)";
                }
            }

        }

////////////////////////////       THE FUNCTION THAT PLOTS THE ROOM GRAPHS          ////////////////////////////////////

        // ANDREW WHATS UP BUDDY
        // At the moment this is fake. You will need to actually generate this data from our database
        // Use the authenticated recordings directly from the log files as the values don't worry about basing plots on predictions too much work.
        // Bottom left graph sucks major balls if you can think of something else awesome

        function multiplePlots(){
////////////////// PLOT 1 STACKED BAR PLOTS
            // Trace 1 is a dictionary. each trace is a plot that will be plot by plotly
            // x: y: attributes gives plotly x and y arrays to make a 2d plot
            // The 'type:' attribute tells plotly that the 2d plot should be a barplot.   'h' means horizontal.
            // xaxis: and yaxis: as opposed to x: y: attributes tells plotly to put the overall plot on the bottom right of our multiple plots
            var trace1 = {
                x: [80,  50,  70,  34,  29,  33,  35,  38,  42,  45,  49,  51,
            53,  56,  60,  65,  66,  73,  74,  79,  84,  96,  98, 103, 107,
           108, 112, 113, 139, 143],
                y: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                xaxis: 'x1',
                yaxis: 'y1',
                name: 'Arrive',
                orientation: 'h',
                type: 'bar'
            };
            var trace11 = {
                x: [100,  80,  90, 80, 60,  27,  96,  42,  29, 143,  51,  35,
            38,  22,  65,  49, 103, 139,  79,  84,  73,  66,  19,  56,  74,
           108, 107,  98,  33,  18],
                y: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                xaxis: 'x1',
                yaxis: 'y1',
                name: 'Registered',
                orientation: 'h',
                type: 'bar'
            };

////////////////// PLOT 2;   6 lines plotted in the same graph.
            //OCCUPANCY ACROSS THE WEEK
            //Six traces here same deal, x values, y values, top right position in muttiple
            var trace4 = {
              x: [1, 2, 3, 4, 5, 6, 7, 8, 9],
              y: [948, 862, 800, 800, 900, 800, 892, 800, 800],
              xaxis: 'x4',
              yaxis: 'y4',
              mode: 'lines',
              type: 'scatter'
            };
            var trace5 = {
              x: [1, 2, 3, 4, 5, 6, 7, 8, 9],
              y: [791, 800, 810, 830, 820, 870, 800, 900, 810],
              xaxis: 'x4',
              yaxis: 'y4',
              mode: 'lines',
              type: 'scatter'
            };
            var trace6 = {
              x: [1, 2, 3, 4, 5, 6, 7, 8, 9],
              y: [862, 900, 900, 800, 800, 850, 900, 1000, 900],
              xaxis: 'x4',
              yaxis: 'y4',
              mode: 'lines',
              type: 'scatter'
            };
            var trace7 = {
              x: [1, 2, 3, 4, 5, 6, 7, 8, 9],
              y: [800, 892, 810, 756, 948, 862, 901, 838, 800],
              xaxis: 'x4',
              yaxis: 'y4',
              mode: 'lines',
              type: 'scatter'
            };
            var KEY = {
              x: [1, 2, 3, 4, 5, 6, 7, 8, 9],
              y: [800, 756, 862, 800, 800, 948, 838, 901, 800],
              xaxis: 'x4',
              yaxis: 'y4',
              name: 'This Week',
              mode: 'lines',
              type: 'scatter'
            };
            var trace9 = {
              x: [1, 2, 3, 4, 5, 6, 7, 8, 9],
              y: [901, 800, 892, 791, 756, 862, 800, 948, 838,],
              xaxis: 'x4',
              yaxis: 'y4',
              mode: 'lines',
              type: 'scatter'
            };

////////////////// BUBBLE PLOT;
            // This is a 3 dimensional plot.
            // x axis is Day of the week. y axis is time of day
            // The size of the bubble is the occupancy. color/opacity/size lets you set the bubble properties.
            // Each trace is a horizontal row of bubbles along the x axis.
            var bubble1 = {
              x: ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00'],
              y: ['Monday', 'Monday', 'Monday', 'Monday', 'Monday', 'Monday', 'Monday', 'Monday', 'Monday'],
              xaxis: 'x2',
              yaxis: 'y2',
              mode: 'markers',
              marker: {
                color: ['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)', 'rgb(255, 65, 54)', 'rgb(100, 20, 95)', 'rgb(255, 65, 54)', 'rgb(100, 20, 95)'],
                opacity: [.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                size: [6, 40, 19, 40, 26, 26, 13]
              }
            };

            var bubble2 = {
              x: ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00'],
              y: ['Tuesday', 'Tuesday', 'Tuesday', 'Tuesday', 'Tuesday', 'Tuesday', 'Tuesday', 'Tuesday', 'Tuesday'],
              xaxis: 'x2',
              yaxis: 'y2',
              mode: 'markers',
              marker: {
                color: ['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)', 'rgb(255, 65, 54)', 'rgb(100, 20, 95)', 'rgb(255, 65, 54)', 'rgb(100, 20, 95)'],
                opacity: [.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                size: [13, 13, 40, 40, 19, 26, 6]
              }
            };

            var bubble3 = {
              x: ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00'],
              y: ['Wednesday', 'Wednesday', 'Wednesday', 'Wednesday', 'Wednesday', 'Wednesday', 'Wednesday', 'Wednesday', 'Wednesday'],
              xaxis: 'x2',
              yaxis: 'y2',
              mode: 'markers',
              marker: {
                color: ['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)', 'rgb(255, 65, 54)', 'rgb(100, 20, 95)', 'rgb(255, 65, 54)', 'rgb(100, 20, 95)'],
                opacity: [.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                size: [6, 40, 19, 6, 6, 19, 19]
              }
            };

////////////////// Simple bar-plot showing aggregate 0/ 25/ 50/ 75/ 100 of the week
            var trace3 = {
                x: ['Empty', 'Quarter', 'Half', 'Two-Thirds', 'Full'],
                y: [20, 30, 10, 25, 15],
                xaxis: 'x3',
                yaxis: 'y3',
                type: 'bar',
                text: ['Classroom is empty', 'Quarter Full', 'Half Full', 'Two Thirds', 'Full Up'],
                marker: {
                    color: ['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)', 'rgb(255, 65, 54)', 'rgb(100, 20, 95)'],
                    opacity: 0.6,
                    line: {
                        color: ['rbg(8,48,107)', 'rbg(8,48,107)', 'rbg(8,48,107)', 'rbg(8,48,107)', 'rbg(8,48,107)'],
                        width: 2
                    }
                }
            };

////////////////// Takes all our traces and puts into 1 big array
            var data = [trace1, trace11, bubble1, bubble2, bubble3, trace3, trace4, trace5, trace6, trace7, KEY, trace9];

////////////////// This layout dixtionary is organising the 4 subplots with positioning titles and whatnot
            var layout = {
              title: 'Room Statistics',
              barmode: 'stack',

              xaxis: {title: 'Registered vs Attendance', domain: [0, 0.45], anchor: 'x1'},
              yaxis: {domain: [0, 0.45]},

              xaxis4: {title: 'Occupancy Throughout Week', domain: [0.55, 1], anchor: 'y4'},
              yaxis4: {domain: [0.55, 1], anchor: 'x4'},

              xaxis3: {title: 'Maura', domain: [0, 0.45], anchor: 'y3'},
              yaxis3: {domain: [0.55, 1]},

              xaxis2: {title: 'Bubble', domain: [0.55, 1]},
              yaxis2: {domain: [0, 0.45], anchor: 'x2'}

            };


////////////////// This line plots the big array with the layout into the graph div
            Plotly.newPlot('graph', data, layout);
        }


//////////////////////////////////   THIS SHOWS AND HIDES THE GRAPH BASED ON CLICKING A ROOM        //////////////////////////
        function changeSelection(item){
            document.getElementById(item).style.border = "solid 2px red";
        }
        function changeBack(item){
            document.getElementById(item).style.border = "solid 0px black";
        }
        function changeAgain(item){
            multiplePlots()
            document.getElementById('graph').style.display = "inline-block";
            document.getElementById('map').style.display = "none";

        }
        function goBack(){
            document.getElementById('graph').style.display = "none";
            document.getElementById('map').style.display = "inline-block";
        }

