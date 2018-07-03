
Highcharts.chart('container', {

    chart: {
        scrollablePlotArea: {
            minWidth: 700
        },
        width: 700
    },



    title: {
        text: 'Sentiment Analysis on Combined International News Articles'
    },

    subtitle: {

    },

    xAxis: {
        tickInterval:  24 * 3600 * 1000, // one week
        tickWidth: 0,
        gridLineWidth: 1,
        type: 'datetime',
        dateTimeLabelFormats:{
          month: '%e. %b',
          year: '%b'
        },

        labels: {
            align: 'right',
            x: 3,
            y: -3
        },
        crosshair: {
          width: 1,
          color: 'black'
      }
    },

    yAxis: [{ // left y axis
        title: {
            text: 'Sentiment Score'
        },
        //max:1,
        //min:-1,

        endOnTick: false,
        labels: {
            align: 'left',
            x: 3,
            y: 16,
            format: '{value:.,0f}'
        },
    }, { // right y axis
        linkedTo: 0,
        gridLineWidth: 0,
        opposite: true,
        title: {
            text: null
        },
        labels: {
            align: 'right',
            x: -3,
            y: 16,
            format: '{value:.,0f}'
        },
    }],
    credits: false,
    legend: {
        align: 'left',
        verticalAlign: 'top',
        borderWidth: 0
    },

    tooltip: {
        shared: true,
        crosshairs: true
    },

    plotOptions: {
        series: {
            cursor: 'pointer',
            point: {
                events: {
                    click: function (e) {
                        hs.htmlExpand(null, {
                            pageOrigin: {
                                x: e.pageX || e.clientX,
                                y: e.pageY || e.clientY
                            },
                            headingText: this.series.name,
                            maincontentText: Highcharts.dateFormat('%A, %b %e, %Y', this.x) + ':<br/> ' +
                                this.y + ' sessions',
                            width: 200
                        });
                    }
                }
            },
            marker: {
                lineWidth: 1
            }
        }
    },

});


Highcharts.chart('area', {
    chart: {
        type: 'area',
        width: 700
    },
    title: {
        text: 'Ratio of Articles Containing the Keyword'
    },

    xAxis: {
        tickInterval:  24 * 3600 * 1000, // one week
        tickWidth: 0,
        gridLineWidth: 1,
        type: 'datetime',
        dateTimeLabelFormats:{
          month: '%e. %b',
          year: '%b'
        },
        labels: {
            align: 'right',
            x: 3,
            y: -3
        },
        crosshair: {
          width: 1,
          color: 'black'
        },

        allowDecimals: false,

    },



    yAxis: [{
        title: {
            text: 'Ratio'
        },
        labels: {
            align: 'left',
            x: 3,
            y: 16,
            format: '{value:.,0f}'
        },
    }, { // right y axis
        linkedTo: 0,
        gridLineWidth: 0,
        opposite: true,
        title: {
            text: null
        },
        labels: {
            align: 'right',
            x: -3,
            y: 16,
            format: '{value:.,0f}'
        },
    }],
    credits: false,
    tooltip: {

        shared: true,
        crosshairs: true
    },
    plotOptions: {
        area: {
            marker: {
                enabled: false,
                symbol: 'circle',
                radius: 2,
                states: {
                    hover: {
                        enabled: true
                    }
                }
            }
        }
    },

});
