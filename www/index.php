<?php // content="text/plain; charset=utf-8"

require_once ('jpgraph/jpgraph.php');
require_once ('jpgraph/jpgraph_line.php');
require_once ('jpgraph/jpgraph_scatter.php');
require_once ('jpgraph/jpgraph_regstat.php');

$db = new PDO('pgsql:dbname=weatherik;host=localhost;user=weatherik_user;password=weatherik_password');


// knmi

$qKnmi = $db->prepare("SELECT date, AVG(temperature_maximum) AS temperature_maximum, AVG(temperature_minimum) AS temperature_minimum, AVG(temperature_average) AS temperature_average FROM source_knmi WHERE date > (CURRENT_DATE - INTERVAL '30 days') GROUP BY date ORDER BY date ASC;");
$qKnmi->execute();
$rowsKnmi = $qKnmi->fetchAll();

$x = array();
$yMinimum = array();
$yMaximum = array();
$yAverage = array();
foreach ($rowsKnmi as $row) {
  $x[] = strtotime($row['date']);
  $yMaximum[] = (float) $row['temperature_maximum'];
  $yMinimum[] = (float) $row['temperature_minimum'];
  $yAverage[] = (float) $row['temperature_average'];
}

$grace = 400000;
$xmin = min($x) - $grace;
$xmax = max($x) + $grace;

$g = new Graph(600, 400);
$g->SetMargin(50, 20, 40, 30);
$g->title->Set("Estimated and actual temperatures");
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

$qYr = $db->prepare("SELECT date, AVG(temperature_minimum) AS temperature_minimum, AVG(temperature_maximum) AS temperature_maximum FROM source_weeronline WHERE day=1 AND date > (CURRENT_DATE - INTERVAL '30 days') GROUP BY date ORDER BY date ASC;");
$qYr->execute();
$rowsYr = $qYr->fetchAll();

$x2 = array();
$y2Min = array();
$y2Max = array();
foreach ($rowsYr as $row) {
  $x2[] = strtotime($row['date']);
  $y2Min[] = (float) $row['temperature_minimum'];
  $y2Max[] = (float) $row['temperature_maximum'];
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

$qYr = $db->prepare("SELECT date, (AVG(temperature_average_1) + AVG(temperature_average_2) + AVG(temperature_average_3) + AVG(temperature_average_4))/4.0 AS temperature_average FROM source_yr WHERE day=1 AND date > (CURRENT_DATE - INTERVAL '30 days') GROUP BY date ORDER BY date ASC;");
$qYr->execute();
$rowsYr = $qYr->fetchAll();

$x1 = array();
$y1 = array();
foreach ($rowsYr as $row) {
  $x1[] = strtotime($row['date']);
  $y1[] = (float) $row['temperature_average'];
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
}
$ymax = max(max($yMaximum), max($y1), max($y2Max)) + 2;
if ($ymax < 0) {
  $ymax = 0;
}

$g->SetScale('intlin', $ymin, $ymax, $xmin, $xmax);
$g->xaxis->SetLabelFormatString('d-m', true);
$g->Stroke();
