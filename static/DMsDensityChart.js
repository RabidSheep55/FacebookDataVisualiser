const users = DMsDensityData.labels.reverse();
const palette = densityPalette.reverse().map((cur) => '#' + cur.map(x => {
  const hex = Math.floor(x * 254).toString(16)
  return hex.length === 1 ? '0' + hex : hex
}).join(''));
const series = DMsDensityData.densities.reverse().reduce((acc, cur, ind) => [...acc, {
  name: DMsDensityData.labels[ind],
  data: cur.map((e, i) => [DMsDensityData.x[i], ind, e * 1.2 + ind]),
  color: palette[ind],
  zIndex: users.length - ind
}], []);

const DMsDensityChart = Highcharts.chart('DMs-density-chart', {
  chart: {
    type: "areasplinerange",
    backgroundColor: "rgba(0, 0, 0, 0)",
    spacingTop: 0,
    plotBorderWidth: 0,
    // spacingRight: 0,
    // spacingBottom: 0,
    // spacingLeft: 0
  },
  title: {
    text: null
  },
  xAxis: {
    type: "datetime",
    labels: {
      style: {
        color: palette[0],
        fontSize: "14px"
      }
    },
    tickColor: palette[0],
    lineColor: palette[0]
  },
  yAxis: {
    title: { text: null },
    categories: users,
    max: users.length,
    labels: {
      useHTML: true,
      formatter: function () {
        if (this.pos < users.length) return `<span style='color: ${palette[this.pos]}'>${this.value}</span>`;
      },
      x: 8,
      y: -8,
      align: 'left',
      style: {
        color: palette[-1],
        fontSize: "14px"
      }
    },
    startOnTick: true,
    gridLineWidth: 0,
    tickmarkPlacement: "off"
  },
  series: series,
  plotOptions: {
    areasplinerange: {
      marker: {
        enabled: false
      },
      fillOpacity: 1,
      // lineColor: palette,
      lineWidth: 2
    },
    series: {
      tooltip: {
        useHTML: true,
        distance: 10,
        headerFormat: '',
        pointFormatter: function () { return `<div style='color: ${this.series.color}'><p><b>Sent:</b> ${DMsDensityData.traceInfo[this.series.name].sent}</p><br><p><b>Received:</b> ${DMsDensityData.traceInfo[this.series.name].received}</p><br><p><b>Total: </b>${DMsDensityData.traceInfo[this.series.name].total}</p></div>` },
        footerFormat: ''
      },
      marker: {
        enabled: false
      },
      enableMouseTracking: true,
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
  legend: {
    enabled: false
  },
  credits: {
    enabled: false
  }
});

setTimeout(function () {
  DMsDensityChart.reflow();
  // chart.redraw();
}, 1)