'use strict';

function constructProjectMarkup(projects) {
    projects.forEach(project => {
        let projectMarkup = d3.select('#projects')
            .insert('li')
            .classed('project', true);
        projectMarkup
            .insert('a')
            .text(project.name)
            .attr('href', `/projects/detail.html?project_id=${project.id}`);
        if (project.description) {
            projectMarkup
                .insert('span')
                .text(project.description);
        } else {
            projectMarkup
                .insert('span')
                .text('No project description')
                .classed('info-secondary', true);
        }
    });
}

window.addEventListener('DOMContentLoaded', e => {
    API_SERVICE.getProjcets()
    .then(response => {
        let projects = response.data;
        constructProjectMarkup(projects);
    })
    .catch(response => {
        console.log(response);
    });
});
