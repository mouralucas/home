var dom = document.getElementById("chart_categorias");
var myChart = echarts.init(dom);
var app = {};
option = null;
option = {
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: ['Valor 1', 'Valor 2', 'Valor 3', 'Valor 4', 'valor 5', 'Valor 6', 'Valor 7', 'Valor 8', 'Valor 9']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: [
        {
            type: 'category',
            data: ['1', '2', '3', '4', '5', '6', '7']
        }
    ],
    yAxis: [
        {
            type: 'value'
        }
    ],
    series: [
        {
            name: 'Valor 1',
            type: 'bar',
            data: [320, 332, 301, 334, 390, 330, 320]
        },
        {
            name: 'Valor 2',
            type: 'bar',
            stack: '广告',
            data: [120, 132, 101, 134, 90, 230, 210]
        },
        {
            name: 'Valor 3',
            type: 'bar',
            stack: '广告',
            data: [220, 182, 191, 234, 290, 330, 310]
        },
        {
            name: 'Valor 4',
            type: 'bar',
            stack: '广告',
            data: [150, 232, 201, 154, 190, 330, 410]
        },
        {
            name: 'Valor 5',
            type: 'bar',
            data: [862, 1018, 964, 1026, 1679, 1600, 1570],
            markLine: {
                lineStyle: {
                    type: 'dashed'
                },
                data: [
                    [{type: 'min'}, {type: 'max'}]
                ]
            }
        },
        {
            name: 'Valor 6',
            type: 'bar',
            barWidth: 5,
            stack: '搜索引擎',
            data: [620, 732, 701, 734, 1090, 1130, 1120]
        },
        {
            name: 'Valor 7',
            type: 'bar',
            stack: '搜索引擎',
            data: [120, 132, 101, 134, 290, 230, 220]
        },
        {
            name: 'Valor 8',
            type: 'bar',
            stack: '搜索引擎',
            data: [60, 72, 71, 74, 190, 130, 110]
        },
        {
            name: 'Valor 9',
            type: 'bar',
            stack: '搜索引擎',
            data: [62, 82, 91, 84, 109, 110, 120]
        }
    ]
};

if (option && typeof option === "object") {
    myChart.setOption(option, true);
}