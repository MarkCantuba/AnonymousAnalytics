'use strict';

const PROJECT_NAME = getQuery('project_name');

document.title = `${PROJECT_NAME} - Project Detail`;

function generateBarChart(data) {
    data.unshift('Event Count');
    c3.generate({
        bindto: '#event-bar-chart',
        data: {
            columns: [data],
            type: 'bar'
        }
    });
}

window.addEventListener('DOMContentLoaded', e => {
    d3.select('#project-name').html([PROJECT_NAME]);

    API_SERVICE.getEvents(PROJECT_NAME)
    .then(response => {
        // generateBarChart(response.data);
        // DUMMY DATA: Unstable API
        generateBarChart([500, 500, 400, 500, 300]);
    })
    .catch(response => {
        console.error(response);
    });
});
