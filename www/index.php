<?php // content="text/plain; charset=utf-8"

require_once ('jpgraph/jpgraph.php');
require_once ('jpgraph/jpgraph_bar.php');
require_once ('jpgraph/jpgraph_line.php');
require_once ('jpgraph/jpgraph_mgraph.php');
require_once ('jpgraph/jpgraph_scatter.php');
require_once ('jpgraph/jpgraph_regstat.php');

function windDirectionToAngle1($direction) {
  switch (strtolower($direction)) {
    case 'north': return 360;
    case 'northwest': return 315;
    case 'west': return 270;
    case 'southwest': return 225;
    case 'south': return 180;
    case 'southeast': return 135;
    case 'east': return 90;
    case 'northeast': return 45;
    default: die('Unknown wind direction: '.$direction);
  }
}

function windDirectionToAngle2($direction) {
  switch (strtolower($direction)) {
    case 'n': return 360;
    case 'nw': return 315;
    case 'w': return 270;
    case 'sw': return 225;
    case 's': return 180;
    case 'se': return 135;
    case 'e': return 90;
    case 'ne': return 45;
    default: die('Unknown wind direction: '.$direction);
  }
}

$db = new PDO('pgsql:dbname=weatherik;host=localhost;user=weatherik_user;password=weatherik_password');


// knmi

$qKnmi = $db->prepare("SELECT date, AVG(temperature_maximum) AS temperature_maximum, AVG(temperature_minimum) AS temperature_minimum, AVG(temperature_average) AS temperature_average, AVG(rain_amount) AS rain_amount, AVG(wind_direction) AS wind_direction FROM source_knmi WHERE date > (CURRENT_DATE - INTERVAL '30 days') GROUP BY date ORDER BY date ASC;");
$qKnmi->execute();
$rowsKnmi = $qKnmi->fetchAll();

$x = array();
$yMinimum = array();
$yMaximum = array();
$yAverage = array();
$yRain = array();
$yWindDirection = array();
foreach ($rowsKnmi as $row) {
  $x[] = strtotime($row['date']);
  $yMaximum[] = (float) $row['temperature_maximum'];
  $yMinimum[] = (float) $row['temperature_minimum'];
  $yAverage[] = (float) $row['temperature_average'];
  $yRain[] = (float) $row['rain_amount'];
  $yWindDirection[] = (int) $row['wind_direction'];
}

$grace = 400000;
$xmin = min($x) - $grace;
$xmax = max($x) + $grace;

$g = new Graph(600, 400);
$g->SetMargin(50, 20, 40, 30);
$g->title->Set("Predicted and actual temperatures");
$g->SetMarginColor('lightblue');

$g->img->SetAntiAliasing();

$lplot = new LinePlot($yMaximum, $x);
$g->Add($lplot);
$lplot->SetLegend('maximum (KNMI)');
$lplot->SetColor('red');

$lplot = new LinePlot($yMinimum, $x);
$g->Add($lplot);
$lplot->SetColor('blue');
$lplot->SetLegend('minimum (KNMI)');

$lplot = new LinePlot($yAverage, $x);
$g->Add($lplot);
$lplot->SetColor('green');
$lplot->SetLegend('average (KNMI)');


// Weeronline

$qYr = $db->prepare("SELECT date, temperature_minimum, temperature_maximum, rain_amount, wind_direction FROM source_weeronline WHERE day=1 AND date > (CURRENT_DATE - INTERVAL '30 days') ORDER BY date ASC;");
$qYr->execute();
$rowsYr = $qYr->fetchAll();

$x2 = array();
$y2Min = array();
$y2Max = array();
$y2Rain = array();
$y2WindDirection = array();
foreach ($rowsYr as $row) {
  $x2[] = strtotime($row['date']);
  $y2Min[] = (float) $row['temperature_minimum'];
  $y2Max[] = (float) $row['temperature_maximum'];
  $y2Rain[] = (float) $row['rain_amount'];
  $y2WindDirection[] = windDirectionToAngle2($row['wind_direction']);
}

$lplot = new ScatterPlot($y2Max, $x2);
$lplot->SetLegend('predicted maximum (Weeronline)');
$lplot->mark->SetType(MARK_UTRIANGLE, '', 1.0);
$lplot->mark->SetColor('red');
$lplot->mark->SetFillColor('red');
$g->Add($lplot);

$lplot = new ScatterPlot($y2Min, $x2);
$lplot->SetLegend('predicted minimum (Weeronline)');
$lplot->mark->SetType(MARK_UTRIANGLE, '', 1.0);
$lplot->mark->SetColor('blue');
$lplot->mark->SetFillColor('blue');
$g->Add($lplot);


// Yr

$qYr = $db->prepare("SELECT date, (temperature_average_1 + temperature_average_2 + temperature_average_3 + temperature_average_4)/4.0 AS temperature_average, rain_amount_1 + rain_amount_2 + rain_amount_3 + rain_amount_4 AS rain_amount, wind_direction_1, wind_direction_2, wind_direction_3, wind_direction_4 FROM source_yr WHERE day=1 AND date > (CURRENT_DATE - INTERVAL '30 days') ORDER BY date ASC;");
$qYr->execute();
$rowsYr = $qYr->fetchAll();

$x1 = array();
$y1 = array();
$y1Rain = array();
$y1WindDirection = array();
foreach ($rowsYr as $row) {
  $x1[] = strtotime($row['date']);
  $y1[] = (float) $row['temperature_average'];
  $y1Rain[] = (float) $row['rain_amount'];
  $y1WindDirection[] = (windDirectionToAngle1($row['wind_direction_1']) +
      windDirectionToAngle1($row['wind_direction_2']) +
      windDirectionToAngle1($row['wind_direction_3']) +
      windDirectionToAngle1($row['wind_direction_4'])) / 4.0;
}

$lplot = new ScatterPlot($y1, $x1);
$lplot->SetLegend('predicted average (Yr)');
$lplot->mark->SetType(MARK_FILLEDCIRCLE, '', 1.0);
$lplot->mark->SetColor('green');
$lplot->mark->SetFillColor('green');
$g->Add($lplot);


// finialize

$ymin = min(min($yMinimum), min($y1), min($y2Min)) - 2;
if ($ymin > 0) {
  $ymin = 0;
} else {
  $ymin = floor($ymin);
}
$ymax = max(max($yMaximum), max($y1), max($y2Max)) + 2;
if ($ymax < 0) {
  $ymax = 0;
} else {
  $ymax = ceil($ymax);
}
$yRainMax = max(max($yRain), max($y1Rain), max($y2Rain)) + 2;
$yRainMax = ceil($yRainMax);

$g->SetScale('intlin', $ymin, $ymax, $xmin, $xmax);
$g->xaxis->SetLabelFormatString('d-m', true);

$mgraph = new MGraph();
$mgraph->Add($g, 5, 5);

$g = new Graph(600, 400);
$g->SetMargin(50, 20, 40, 30);
$g->title->Set("Predicted and actual amount of rain");
$g->SetMarginColor('lightblue');

$plot = new BarPlot($yRain, $x);
$g->Add($plot);
$plot->SetAlign('center');
$plot->SetAbsWidth(32);
$plot->SetLegend('measured (KNMI)');
$plot->SetColor('blue');

$lplot = new ScatterPlot($y1Rain, $x1);
$lplot->SetLegend('predicted (Yr)');
$lplot->mark->SetType(MARK_FILLEDCIRCLE, '', 1.0);
$lplot->mark->SetColor('green');
$lplot->mark->SetFillColor('green');
$g->Add($lplot);

$lplot = new ScatterPlot($y2Rain, $x2);
$lplot->SetLegend('predicted (Weeronline)');
$lplot->mark->SetType(MARK_UTRIANGLE, '', 1.0);
$lplot->mark->SetColor('red');
$lplot->mark->SetFillColor('red');
$g->Add($lplot);

$g->SetScale('intlin', 0, $yRainMax, $xmin, $xmax);
$g->xaxis->SetLabelFormatString('d-m', true);

$mgraph->Add($g, 5, 405);

$g = new Graph(600, 400);
$g->SetMargin(50, 20, 40, 30);
$g->title->Set("Predicted and actual wind direction");
$g->SetMarginColor('lightblue');

$lplot = new LinePlot($yWindDirection, $x);
$g->Add($lplot);
$lplot->SetColor('gray');
$lplot->SetLegend('measured (KNMI)');

$lplot = new ScatterPlot($y2WindDirection, $x2);
$lplot->SetLegend('predicted (Weeronline)');
$lplot->mark->SetType(MARK_UTRIANGLE, '', 1.0);
$lplot->mark->SetColor('red');
$lplot->mark->SetFillColor('red');
$g->Add($lplot);

$lplot = new ScatterPlot($y1WindDirection, $x1);
$lplot->SetLegend('predicted (Yr)');
$lplot->mark->SetType(MARK_FILLEDCIRCLE, '', 1.0);
$lplot->mark->SetColor('green');
$lplot->mark->SetFillColor('green');
$g->Add($lplot);

$g->SetScale('intlin', 0, 360, $xmin, $xmax);
$g->xaxis->SetLabelFormatString('d-m', true);

$mgraph->Add($g, 5, 810);
$mgraph->Stroke();
