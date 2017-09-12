/**
 * Created by xuJL on 2017/7/31.
 */
$(document).ready(function () {
    //alert("#select-dev").length);
    if($("#select-dev").length>0){
    }
    init();
    getTerminal();
});

function getTerminal() {
    var head = $("#climate-head");
    var body = $("#climate-body");

    if(head.text()!==null || body.text()!==null){
        head.empty();
        body.empty();
    }
    var dev = $("#select-dev").val();
    var term = $("#"+dev).val();
    var date = $("#select-date").val();
    if(term!==undefined && date!==undefined){
        getClimateDay(term, date);
    }
}

// function getDate(id) {
//     getTerminal();
// }

function getClimateDay(terminalid,date) {
    $.ajax({
        type:"get",
        dataType:"json",
        url:"/terminals/"+terminalid+"/climate/day/"+date+"/",
        beforeSend: function(request) {
            request.setRequestHeader("Authorization", "Token ef1ea763ba650c3f2729b68a9384b972639c3aa2");
        },
        success:function (msg) {
            if(msg){
                asTable(msg);
            }
        }
    })
}


function getWeekClimate() {
    var head = $("#climate-week-head");
    var body = $("#climate-week-body");

    if(head.text()!==null || body.text()!==null){
        head.empty();
        body.empty();
    }
    //end = new Date().Format("yyyy-MM-dd");
    end = $("#select-date").val();
    begin = parseDate(end);
    var dev = $("#select-dev").val();
    var terminalid = $("#"+dev).val();
    if(terminalid!==undefined ){
       $.ajax({
        type:"get",
        dataType:"json",
        url:"/terminals/"+terminalid+"/climate/days/"+begin+"/"+end+"/",
        beforeSend: function(request) {
            request.setRequestHeader("Authorization", "Token ef1ea763ba650c3f2729b68a9384b972639c3aa2");
        },
        success:function (msg) {
            if(msg){
                asChart(msg, begin, end);
            }
        }
        })
    }
}

function asTable(msg) {
    var row= "";
    var body = [];
    var net = "";
    var inner = "";
    var date = "";
    $.each(msg, function (index, obj) {
        //console.log(index+":"+obj);
        row+="<tr>";
        //row+="<td>"+obj.date+"</td>";
        date = obj.date;
        row+="<td>"+obj.time.substr(0,5)+"</td>";

        (obj.temp_net === null) ? net="": net=obj.temp_net;
        row+="<td>"+net+"</td>";

        (obj.temp_inner === null) ? inner="": inner=obj.temp_inner;
        row+="<td>"+inner+"</td>";
        row+="</tr>";
        body.push(row);
        row =""
    });
    //var head = "<tr><td>日期</td><td>时间</td><td>预报温度</td><td>室内温度</td></tr>";
    var head = "<tr><th>时间</th><th>预报温度</th><th>室内温度</th></tr>";
    if(body.length!==0){
        $("#climate-head").append(head);
        $("#climate-body").append(body);

        $('#container1').highcharts({
        data: {
            table: 'climate-day-tb'
            //table: 'datatable'
        },
        chart: {
            type: 'column'
        },
        title: {
            text: '24小时预报与室内温度对比 ('+date+')'
        },
        yAxis: {
            allowDecimals: false,
            title: {
                text: '℃',
                rotation: 0
            }
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                    this.point.y + ' ℃' + this.point.name.toLowerCase();
            }
        }
    });
    }
}

function asChart(msg) {
    var row= "";
    var body = [];
    var net = "";
    var inner = "";
    var date = "";
    $.each(msg, function (index, obj) {
        //console.log(index+":"+obj);
        row+="<tr>";
        //row+="<td>"+obj.date+"</td>";
        row+="<td>"+obj.date+"</td>";

        (obj.avg_net === null) ? net="": net=obj.avg_net;
        row+="<td>"+net+"</td>";

        (obj.avg_inner === null) ? inner="": inner=obj.avg_inner;
        row+="<td>"+inner+"</td>";
        row+="</tr>";
        body.push(row);
        row =""
    });
    //var head = "<tr><td>日期</td><td>时间</td><td>预报温度</td><td>室内温度</td></tr>";
    var head = "<tr><th>日期</th><th>预报均值</th><th>室温均值</th></tr>";
    if(body.length!==0){
        $("#climate-week-head").append(head);
        $("#climate-week-body").append(body);

        $('#container2').highcharts({
        data: {
            table: 'climate-week-tb'
        },
        chart: {
            type: 'column'
        },
        title: {
            text: '一周预报温度与室温均值对比 ('+begin+' ~ '+end.substr(5,5)+')'
        },
        yAxis: {
            allowDecimals: false,
            title: {
                text: '℃',
                rotation: 0
            }
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.series.name + '</b><br/>' +
                    this.point.y + ' ℃';
            }
        }
    });
    }
}

function init() {
    var now = new Date().Format("yyyy-MM-dd");
    $("#select-date").val(now)
}

function parseDate(now) {
    //var option = "";
    //var now = new Date().toLocaleDateString().split("/");
    //var now = new Date().Format("yyyy-MM-dd").split("-");
    //alert(now);
    now = now.split("-");
    now = new Date(Number(now[0]), (Number(now[1])-1), Number(now[2]));

    //console.log(now.setDate(now.getDate()-1));
    //alert(now.Format("yyyy-MM-dd"));
    now.setDate(now.getDate()-6);
    return now.Format("yyyy-MM-dd");

    //
    // for(var i=0;i<8;i++){
    //     if(i===0) {
    //         option+="<option>"+now.Format("yyyy-MM-dd")+"</option>";
    //     }else if(i<7){
    //         now.setDate(now.getDate()-1);
    //         option+="<option>"+now.Format("yyyy-MM-dd")+"</option>";
    //     }else {
    //         option+="<option onclick=\"return Calendar('time')\"></option>";
    //     }
    //
    // }
    // $("#select-date").append(option);
}

Date.prototype.Format = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
};

//3d  柱状图
$(function () {
    $("#select-date").datetimepicker({
        language: 'zh-CN',
        format: "yyyy-mm-dd",
        weekStart: 1,
        startView: 2,
        minView: 2,
        autoclose: true,
        todayBtn: true,
        pickerPosition: "bottom-right",
    }).on("click", function () {
        $("#select-date").datetimepicker("show")
    })
    // $('#container').highcharts({
    //     chart: {
    //         type: 'column',
    //         options3d: {
    //             enabled: true,
    //             alpha: 15,
    //             beta: 15,
    //             viewDistance: 25,
    //             depth: 40
    //         },
    //         marginTop: 80,
    //         marginRight: 40
    //     },
    //     title: {
    //         text: '日气温对比'
    //     },
    //     xAxis: {
    //         categories: ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', ]
    //     },
    //     yAxis: {
    //         allowDecimals: false,
    //         min: 0,
    //         title: {
    //             text: '温度值'
    //         }
    //     },
    //     tooltip: {
    //         headerFormat: '<b>{point.key}</b><br>',
    //         pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: {point.y} / {point.stackTotal}'
    //     },
    //     plotOptions: {
    //         column: {
    //             stacking: 'normal',
    //             depth: 40
    //         }
    //     },
    //     series: [{
    //         name: '小张',
    //         data: [5, 3, 4, 7, 2],
    //         stack: 'male'
    //     }, {
    //         name: '小王',
    //         data: [3, 4, 4, 2, 5],
    //         stack: 'male'
    //     }, {
    //         name: '小彭',
    //         data: [2, 5, 6, 2, 1],
    //         stack: 'female'
    //     }, {
    //         name: '小潘',
    //         data: [3, 0, 4, 4, 3],
    //         stack: 'female'
    //     }]
    // });
    //
    // $('#container3').highcharts({
    //     chart: {
    //         type: 'column'
    //     },
    //     title: {
    //         text: '月平均降雨量'
    //     },
    //     subtitle: {
    //         text: '数据来源: WorldClimate.com'
    //     },
    //     xAxis: {
    //         categories: [
    //             '一月',
    //             '二月',
    //             '三月',
    //             '四月',
    //             '五月',
    //             '六月',
    //             '七月',
    //             '八月',
    //             '九月',
    //             '十月',
    //             '十一月',
    //             '十二月'
    //         ],
    //         crosshair: true
    //     },
    //     yAxis: {
    //         min: 0,
    //         title: {
    //             text: '降雨量 (mm)'
    //         }
    //     },
    //     tooltip: {
    //         headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
    //         pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
    //         '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
    //         footerFormat: '</table>',
    //         shared: true,
    //         useHTML: true
    //     },
    //     plotOptions: {
    //         column: {
    //             pointPadding: 0.2,
    //             borderWidth: 0
    //         }
    //     },
    //     series: [{
    //         name: '东京',
    //         data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
    //     }, {
    //         name: '纽约',
    //         data: [83.6, 78.8, 98.5, 93.4, 106.0, 84.5, 105.0, 104.3, 91.2, 83.5, 106.6, 92.3]
    //     }, {
    //         name: '伦敦',
    //         data: [48.9, 38.8, 39.3, 41.4, 47.0, 48.3, 59.0, 59.6, 52.4, 65.2, 59.3, 51.2]
    //     }, {
    //         name: '柏林',
    //         data: [42.4, 33.2, 34.5, 39.7, 52.6, 75.5, 57.4, 60.4, 47.6, 39.1, 46.8, 51.1]
    //     }]
    // });


});
