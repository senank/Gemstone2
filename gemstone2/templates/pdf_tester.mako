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
        
        <div class = 'row' style = 'margin: 10px; height: 50px; border-style: solid; border-width: 1px;'>
            <div class = "col-md-2" style = "padding: 15px; height : 130px;">Company:</div>
            <div class = "col-md-2" style = "padding: 15px; height : 130px;">${report.company}</div>
            <div class = "col-md-2" style = "padding: 15px; height : 130px;"></div>
            <div class = "col-md-2" style = "padding: 15px; height : 130px;"></div>
            <div class = "col-md-2" style = "padding: 15px; height : 130px;">Quarter:</div>
            <div class = "col-md-1" style = "padding: 15px; height : 130px;">${report.quarter}</div>
            <div class = "col-md-1" style = "padding: 15px; height : 130px;">${report.year}</div>
        </div>

        <div class = 'row' style = "margin: 10px;">
            <div class = "col-md-12 text-center" style = "padding: 15px; height : 225px; border-style: solid; border-width: 1px;"><h5 style = "text-decoration: underline;">Industry & Business Major Highlights</h5>
                <ul>
                    <li><div class = 'row'>${report.highlight1}</div></li>
                    <li><div class = 'row'>${report.highlight2}</div></li>
                    <li><div class = 'row'>${report.highlight3}</div></li>
                    <li><div class = 'row'>${report.highlight4}</div></li>
                    <li><div class = 'row'>${report.highlight5}</div></li>
                    <li><div class = 'row'>${report.highlight6}</div></li>
                    <li><div class = 'row'>${report.highlight7}</div></li>
                </ul>
                ## <div class = 'row'>${report.highlight8}</div>
                ## <div class = 'row'>${report.highlight9}</div>
            </div>
        </div>
        
        <div class = 'row' style = "margin: 10px;">
            <div class = "col-md-6 text-center" style = "padding: 15px; height : 150px; border-style: solid; border-width: 1px;"><h5 style = "text-decoration: underline;">Operations Update</h5>
                <ul>
                    <li><div class = 'row'>${report.operation1}</div></li>
                    <li><div class = 'row'>${report.operation2}</div></li>
                    <li><div class = 'row'>${report.operation3}</div></li>
                    <li><div class = 'row'>${report.operation4}</div></li>
                </ul>
            </div>
            <div class = "col-md-6 text-center" style = "padding: 15px; height : 150px; border-style: solid; border-width: 1px;"><h5 style = "text-decoration: underline;">Strategic Initiative Update</h5>
                <ul>
                    <li><div class = 'row'>${report.strategy1}</div></li>
                    <li><div class = 'row'>${report.strategy1}</div></li>
                    <li><div class = 'row'>${report.strategy1}</div></li>
                    <li><div class = 'row'>${report.strategy1}</div></li>
                </ul>
            </div>
        </div>

        <div class = 'row' style = "margin: 10px;">
            <div class = "col-md-6 text-center" style = "padding: 15px; height : 150px; border-style: solid; border-width: 1px;"><h5 style = "text-decoration: underline;">New Customers Gained During Quarter</h5>
                <ul>
                    <li><div class = 'row'>${report.customer_gained1}</div></li>
                    <li><div class = 'row'>${report.customer_gained2}</div></li>
                    <li><div class = 'row'>${report.customer_gained3}</div></li>
                    <li><div class = 'row'>${report.customer_gained4}</div></li>
                </ul>
            </div>
            <div class = "col-md-6 text-center" style = "padding: 15px; height : 150px; border-style: solid; border-width: 1px;"><h5 style = "text-decoration: underline;">Major Orders Received During Quarter</h5>
                <ul>
                    <li><div class = 'row'>${report.order1}</div></li>
                    <li><div class = 'row'>${report.order2}</div></li>
                    <li><div class = 'row'>${report.order3}</div></li>
                    <li><div class = 'row'>${report.order4}</div></li>
                </ul>
            </div>
        </div>


        <h4 class = 'text-center' style = 'margin: 15px;padding: 5px;'>Financial Performance VS. Plan</h4>
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
                        <th>Revenue</th>
                        <th>${report.revenue_1}</th>
                        <th>${report.revenue_2}</th>
                        <th>${report.revenue_3}</th>
                        <th>${report.revenue_4}</th>
                        <th>${report.revenue_YTD}</th>
                        <th>${report.revenue_FY}</th>
                        <th>${report.revenue_plan}</th>
                    </tr>

                    <tr>
                        <th>Gross Profit</th>
                        <th>${report.profit_1}</th>
                        <th>${report.profit_2}</th>
                        <th>${report.profit_3}</th>
                        <th>${report.profit_4}</th>
                        <th>${report.profit_YTD}</th>
                        <th>${report.profit_FY}</th>
                        <th>${report.profit_plan}</th>
                    </tr>

                    <tr>
                        <th>EBITDA</th>
                        <th>${report.EBITDA_1}</th>
                        <th>${report.EBITDA_2}</th>
                        <th>${report.EBITDA_3}</th>
                        <th>${report.EBITDA_4}</th>
                        <th>${report.EBITDA_YTD}</th>
                        <th>${report.EBITDA_FY}</th>
                        <th>${report.EBITDA_plan}</th>
                    </tr>

                    <tr>
                        <th>Free Cash Flow</th>
                        <th>${report.cf_1}</th>
                        <th>${report.cf_2}</th>
                        <th>${report.cf_3}</th>
                        <th>${report.cf_4}</th>
                        <th>${report.cf_YTD}</th>
                        <th>${report.cf_FY}</th>
                        <th>${report.cf_plan}</th>
                    </tr>
                </tbody>
            </table>
        </div>
        %if kpis:
            <div style = "margin: 10px;">
            <h4 class = 'text-center' style = 'margin: 15px;padding: 5px; text-decoration: underline;'>Key Performance Indicators</h4>
            ## <div class = row>
                <div class = 'row text-center'>
                    <div class = "col-md-8 text-left" style = "padding: 15px; height : 30px; text-decoration: underline;">KPI</div>
                    <div class = "col-md-2" style = "padding: 15px; height : 30px; text-decoration: underline;">Value</div>
                    <div class = "col-md-2" style = "padding: 15px; height : 30px; text-decoration: underline;">Target</div>
                </div>
            %for kpi in kpis:
                <div class = 'row text-center'>
                    <div class = "col-md-8 text-left" style = "padding: 15px; height : 30px;">${kpi.kpi_name}</div>
                    <div class = "col-md-2" style = "padding: 15px; height : 30px;">${kpi.value}</div>
                    <div class = "col-md-2" style = "padding: 15px; height : 30px;">${kpi.target}</div>
                </div>
            %endfor
            ## </div>
            </div>
        %endif
    </div>
</body>
</html>