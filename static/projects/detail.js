'use strict';

const PROJECT_ID = getQuery('project_id');

document.title = `${PROJECT_ID} - Project Detail`;

let end = luxon.DateTime.utc();
let start = end.minus({days: 7});
let interval = 21600;

function generateBarChart(data) {
    let timeseries = ['Time Interval'];
    let time = start;
    for (let i = 0; i < data.length; i++) {
        timeseries.push(time.toJSDate());
        time = time.plus({seconds: interval});
    }
    data.unshift('Event Count');
    c3.generate({
        bindto: '#event-bar-chart',
        data: {
            x: 'Time Interval',
            columns: [timeseries, data],
            type: 'bar'
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    culling: {
                        max: 5
                    },
                    format: '%Y-%m-%d %H:%M:%S'
                }
            }
        }
    });
}

window.addEventListener('DOMContentLoaded', e => {
    d3.select('#project-name').html([PROJECT_ID]);

    API_SERVICE.getEventCounts(PROJECT_ID, start, end, interval)
    .then(response => {
        generateBarChart(response.data);
    })
    .catch(response => {
        console.error(response);
    });

    d3.select('#period-change').on('change', e=> {
        console.log("1");
        var period = document.getElementById("period-change");
        var periodValue = encodeURIComponent(period.value);
        start = end.minus({days: periodValue});
        API_SERVICE.getEventCounts(PROJECT_ID, start, end, interval)
        .then(response => {
            generateBarChart(response.data);
        })
        .catch(response => {
            console.error(response);
        });
    });
});
