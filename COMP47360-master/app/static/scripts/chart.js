


google.charts.load('current', {packages: ['corechart', 'line', 'bar']});
google.charts.setOnLoadCallback(drawCurveTypes);
google.charts.setOnLoadCallback(drawBasic);


function drawCurveTypes() {
      var data = new google.visualization.DataTable();
      data.addColumn('number', 'X');
      data.addColumn('number', 'Attendance');
     
      data.addRows([
        [0, 20],    [1, 55],   [2, 50],  [3, 52],   [4, 46],  [5, 44],
        [6, 34],    [7, 40],   [8, 45],  [9, 35],   [10, 24],  [11, 9],
		[12, 0],    [13, 55],   [14, 50],  [15, 52],   [16, 46],  [17, 44],
        [18, 34],    [19, 40],   [20, 45],  [21, 35],   [22, 24],  [23, 9]
      ]);

      var options = {
        hAxis: {
          title: 'Day (over the semester)'
        },
        vAxis: {
          title: 'Students'
        },
        series: {
          1: {curveType: 'function'}
        }
      };

      var chart = new google.visualization.LineChart(document.getElementById('chart'));
      chart.draw(data, options);
    }



function drawBasic() {

      var data = new google.visualization.DataTable();
      data.addColumn('timeofday', 'Time of Day');
      data.addColumn('number', 'Attendance Level');

      data.addRows([
        [{v: [9, 0, 0], f: '9 am'}, 12],
        [{v: [10, 0, 0], f:'10 am'}, 18],
        [{v: [11, 0, 0], f: '11 am'}, 26],
        [{v: [12, 0, 0], f: '12 pm'}, 48],
        [{v: [13, 0, 0], f: '1 pm'}, 54],
        [{v: [14, 0, 0], f: '2 pm'}, 42],
        [{v: [15, 0, 0], f: '3 pm'}, 42],
        [{v: [16, 0, 0], f: '4 pm'}, 36],
        [{v: [17, 0, 0], f: '5 pm'}, 18],
      ]);

      var options = {
        title: 'Attendance Level Throughout the Day',
        hAxis: {
          title: 'Time of Day',
          format: 'h:mm a',
          viewWindow: {
            min: [9, 30, 0],
            max: [17, 30, 0]
          }
        },
        vAxis: {
          title: 'Students'
        }
      };

      var chart = new google.visualization.ColumnChart(
        document.getElementById('columns'));

      chart.draw(data, options);
    }
