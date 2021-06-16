const simpleMessageColours = {
  sent: "#636e72",
  received: "#2d3436",
  labels: "#dfe6e9",
  gridLines: "#00b894"
};

const topUsers = simpleMessageData.reduce((acc, cur) => [...acc, cur[0]], []);
const simpleMessageSeries = simpleMessageData.reduce((acc, cur) => {
  acc[0]['data'].push(cur[1]);
  acc[1]['data'].push(cur[2]);
  return acc;
}, [{ name: 'Sent', data: [], color: simpleMessageColours.sent, borderColor: simpleMessageColours.sent }, { name: 'Received', data: [], color: simpleMessageColours.received, borderColor: simpleMessageColours.received }])

const chart = Highcharts.chart('simple-messages-chart', {
  chart: {
    type: 'bar',
    backgroundColor: "rgba(0, 0, 0, 0)",
    spacingTop: 0,
    spacingRight: 0,
    spacingBottom: 0,
    spacingLeft: -1,
    plotBorderWidth: 0
  },
  xAxis: {
    categories: topUsers,
    minPadding: 0,
    labels: {
      align: "left",
      padding: 0,
      x: 8,
      y: 6,
      style: {
        color: simpleMessageColours.labels,
        whiteSpace: 'nowrap',
        fontSize: "15px"
      }
    },
    lineColor: "rgba(0, 0, 0, 0)",
  },
  yAxis: {
    title: {
      text: null
    },
    maxPadding: 0,
    showFirstLabel: false,
    endOnTick: false,
    gridLineColor: simpleMessageColours.gridLines,
    gridLineDashStyle: 'dash',
    gridLineWidth: 2,
    labels: {
      style: {
        color: simpleMessageColours.gridLines,
        fontSize: "14px",
        fontWeight: "bold"
      }
    }
  },
  series: simpleMessageSeries,
  plotOptions: {
    series: {
      stacking: "normal",
      states: {
        inactive: {
          opacity: 1
        },
        hover: {
          enabled: false
        }
      }
    }
  },
  title: {
    text: null
  },
  legend: {
    enabled: false
  },
  credits: {
    enabled: false
  }
});

setTimeout(function () {
  chart.reflow();
  // chart.redraw();
}, 1)