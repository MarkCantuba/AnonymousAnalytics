'use strict';

const PROJECT_ID = getQuery('project_id');

document.title = `${PROJECT_ID} - Project Detail`;

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

/*
window.addEventListener('DOMContentLoaded', e => {
    d3.select('#project-name').html([PROJECT_ID]);

    API_SERVICE.getEvents(PROJECT_ID)
    .then(response => {
        // generateBarChart(response.data);
        // DUMMY DATA: Unstable API
        generateBarChart([500, 500, 400, 500, 300]);
    })
    .catch(response => {
        console.error(response);
    });
});
*/




window.addEventListener('DOMContentLoaded', e => {
    d3.select('#project-name').html([PROJECT_NAME]);

    API_SERVICE.getEvents(PROJECT_NAME, '2020-10-13T00:00:00Z', '2020-10-20T00:00:00Z', 1)
    .then(response => {
        // generateBarChart(response.data);
        // DUMMY DATA: Unstable API

        let response_array = response.data

        console.log(response_array)

        generateBarChart(response_array);
    })
    .catch(response => {
        console.error(response);
    });
});
