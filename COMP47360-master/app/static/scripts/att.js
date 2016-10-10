
//Calls to Google Chart functions below
google.charts.load('current', {packages: ['controls', 'corechart', 'bar', 'line', 'table']});
google.charts.setOnLoadCallback(drawCurveTypes);
google.charts.setOnLoadCallback(drawBasic1);
google.charts.setOnLoadCallback(drawBasic2);
google.charts.setOnLoadCallback(drawBasic3);

function drawCurveTypes() {
	//Draws a line chart showing Attendance Over the Semester
	var data = new google.visualization.DataTable();
	data.addColumn('number', 'X');
	data.addColumn('number');
	
	var p = 55;
	data.addRows([
		[0, 0],    [1, p],   [2, 50],  [3, 52],   [4, 46],  [5, 44],
		[6, 34],    [7, 40],   [8, 45],  [9, 35],   [10, 24]	
	]);

	var options = {
		hAxis: {
		  title: 'Day'
		},
		series: {
		  1: {curveType: 'function'}
		}
	};

	var chart = new google.visualization.LineChart(document.getElementById('container-fluid'));
	chart.draw(data, options);
}
	
function drawBasic1() {
	//Draws a bar chart showing Attendance By Time of Day
	var data = new google.visualization.DataTable();
	data.addColumn('timeofday', 'Time of Day');
	data.addColumn('number');

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
		title: '',
		hAxis: {
		  title: 'Time of Day',
		  format: 'h:mm a',
		  viewWindow: {
			min: [9, 30, 0],
			max: [17, 30, 0]
		  }
		},
	};

	var chart = new google.visualization.ColumnChart(
		document.getElementById('columns1'));

	chart.draw(data, options);
}

function drawBasic2() {
	//Draws a bar chart showing Attendance By Day of Week
	var data = google.visualization.arrayToDataTable([
		 ['', '', { role: 'style' }],
		 ['Monday', 65, '#3366CC'],           
		 ['Tuesday', 75, '#3366CC'],            
		 ['Wednesday', 82, '#3366CC'],
		 ['Thursday', 85, '#3366CC'], 
		 ['Friday', 45, '#3366CC'], 
	]);
	
	var chart = new google.visualization.ColumnChart(
		document.getElementById('columns2'));

	chart.draw(data);
}

function drawBasic3() {
	//Draws a bar chart showing Student Attendance 
	var data = google.visualization.arrayToDataTable([
		 ['', '', { role: 'style' }],
		 ['0-20', 3, 'yellow'],           
		 ['20-40', 4, 'yellow'],            
		 ['40-60', 2, 'yellow'],
		 ['60-80', 10, 'yellow'], 
		 ['80-100', 50, 'yellow'], 
	]);

	var options = {
		legend: {position: 'none'}
	};
	
	var chart = new google.visualization.ColumnChart(
		document.getElementById('columns3'));

	chart.draw(data, options);
}

// Used to trigger a dropdown for the menu icon
$(document).ready(function () {
    var trigger = $('.hamburger'),
      overlay = $('.overlay'),
      isClosed = false;

    trigger.click(function () {
      hamburger_cross();      
    });

	function hamburger_cross() {
		if (isClosed == true) {          
			overlay.hide();
			trigger.removeClass('is-open');
			trigger.addClass('is-closed');
			isClosed = false;
		} else {   
			overlay.show();
			trigger.removeClass('is-closed');
			trigger.addClass('is-open');
			isClosed = true;
		}
	}
  
  $('[data-toggle="offcanvas"]').click(function () {
        $('#wrapper').toggleClass('toggled');
  });  
});



