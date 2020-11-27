'use strict';

const DEFAULT_RECENT_DAYS = [
    { recent: 1, interval: 3600 },
    { recent: 3, interval: 10800 },
    { recent: 7, interval: 21600 },
    { recent: 15, interval: 43200 },
    { recent: 30, interval: 86400 }
];

const PROJECT_ID = getQuery('project_id');

let end = luxon.DateTime.utc();
let start = end.minus({days: 7});
let interval = 21600;
let eventType = '';

function generateBarChart(data) {
    let timeseries = ['Time Interval'];
    let time = start;
    for (let i = 0; i < data.length; i++) {
        timeseries.push(time.toJSDate());
        time = time.plus({seconds: interval});
    }
    let eventTypeLabel = 'Event Count';
    if (eventType) {
        eventTypeLabel = `"${eventType}" ` + eventTypeLabel;
    }
    data.unshift(eventTypeLabel);
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

function updateChart() {
    API_SERVICE.getEventCounts(PROJECT_ID, eventType, start, end, interval)
    .then(response => {
        generateBarChart(response.data);
    })
    .catch(response => {
        console.error(response);
    });
}

window.addEventListener('DOMContentLoaded', e => {
    API_SERVICE.getProject(PROJECT_ID)
    .then(response => {
        let project = response.data;
        document.title = `${project.name} - Project Detail`;
        d3.select('.breadcrumb > li:last-child a')
            .text(project.name)
            .attr('href', `/projects/detail.html?project_id=${PROJECT_ID}`);
        d3.select('#project-name')
            .text(project.name);

        updateChart();

        d3.select('#apply-filter').on('click', () => {
            let recentDays = parseInt(d3.select('#period-change').property('value'));
            interval = DEFAULT_RECENT_DAYS.find(s => s.recent === recentDays).interval;
            end = luxon.DateTime.utc();
            start = end.minus({days: recentDays});
            eventType = d3.select('#event-type-filter').property('value');

            updateChart();
        });
    })
    .catch(response => {
        console.error(response);
        d3.select('.breadcrumb > li:last-child a')
            .text('Not Found');
        d3.select('#project-name')
            .text('Project Not Found');
    });
});
