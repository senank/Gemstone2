<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    <link href="${request.static_url('gemstone2:static/pdf.css')}" rel="stylesheet">
    <title>Document</title>
</head>
<body>
    <div class = 'container'>
        <h2 class = 'text-center' style = 'margin: 15px;padding: 5px;'>GEMSTONE II</h2>
        
        <div class = 'row' style = 'height: 50px;'>
            <div class = "col-md-2" style = "padding: 15px; height : 130px;">Company</div>
            <div class = "col-md-2" style = "padding: 15px; height : 130px;">${report.company}</div>
            <div class = "col-md-2" style = "padding: 15px; height : 130px;"></div>
            <div class = "col-md-2" style = "padding: 15px; height : 130px;"></div>
            <div class = "col-md-2" style = "padding: 15px; height : 130px;">Quarter</div>
            <div class = "col-md-1" style = "padding: 15px; height : 130px;">${report.quarter}</div>
            <div class = "col-md-1" style = "padding: 15px; height : 130px;">${report.year}</div>
        </div>

        <div class = 'row'>
            <div class = "col-md-12 text-center" style = "padding: 15px; height : 200px;">Industry & Business Major Highlights
                <div class = 'row'>${report.highlight1}</div>
                <div class = 'row'>${report.highlight2}</div>
                <div class = 'row'>${report.highlight3}</div>
                <div class = 'row'>${report.highlight4}</div>
                <div class = 'row'>${report.highlight5}</div>
                <div class = 'row'>${report.highlight6}</div>
                <div class = 'row'>${report.highlight7}</div>
                ## <div class = 'row'>${report.highlight8}</div>
                ## <div class = 'row'>${report.highlight9}</div>
            </div>
        </div>
        
        <div class = 'row'>
            <div class = "col-md-6" style = "padding: 15px; height : 130px;">Operations Update</div>
            <div class = "col-md-6" style = "padding: 15px; height : 130px;">Strategic Initiative Update</div>
        </div>

        <div class = 'row'>
            <div class = "col-md-6" style = "padding: 15px; height : 130px;">New Customers Gained During Quarter</div>
            <div class = "col-md-6" style = "padding: 15px; height : 130px;">Major Orders Received During Quarter</div>
        </div>


        <h4 class = 'text-center'>Financial Performance VS. Plan</h4>
        <div class = "table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Q1 Actual</th>
                        <th>Q2 Actual</th>
                        <th>Q3 Actual</th>
                        <th>Q4 Actual</th>
                        <th>YTD Actual</th>
                        <th>% of FY Plan</th>
                        <th>FY Plan</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <th></th>
                        <th>Q1 Actual</th>
                        <th>Q2 Actual</th>
                        <th>Q3 Actual</th>
                        <th>Q4 Actual</th>
                        <th>YTD Actual</th>
                        <th>% of FY Plan</th>
                        <th>FY Plan</th>
                    </tr>

                    <tr>
                        <th></th>
                        <th>Q1 Actual</th>
                        <th>Q2 Actual</th>
                        <th>Q3 Actual</th>
                        <th>Q4 Actual</th>
                        <th>YTD Actual</th>
                        <th>% of FY Plan</th>
                        <th>FY Plan</th>
                    </tr>

                    <tr>
                        <th></th>
                        <th>Q1 Actual</th>
                        <th>Q2 Actual</th>
                        <th>Q3 Actual</th>
                        <th>Q4 Actual</th>
                        <th>YTD Actual</th>
                        <th>% of FY Plan</th>
                        <th>FY Plan</th>
                    </tr>

                    <tr>
                        <th></th>
                        <th>Q1 Actual</th>
                        <th>Q2 Actual</th>
                        <th>Q3 Actual</th>
                        <th>Q4 Actual</th>
                        <th>YTD Actual</th>
                        <th>% of FY Plan</th>
                        <th>FY Plan</th>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class = 'row'>
            <div class = "col-md-12" style = "padding: 15px; height : 200px;">fdas</div>
        </div>
        %for kpi in kpis:
            <div class = 'row text-center'>
                <div class = "col-md-8 text-left" style = "padding: 15px; height : 130px;">${kpi.kpi_name}</div>
                <div class = "col-md-2" style = "padding: 15px; height : 130px;">${kpi.value}</div>
                <div class = "col-md-2" style = "padding: 15px; height : 130px;">${kpi.target}</div>
            </div>
        %endfor
    </div>
</body>
</html>