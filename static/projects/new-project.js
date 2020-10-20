'use strict';

document.addEventListener('DOMContentLoaded', e => {
    d3.select('#new-project-form').on('submit', () => {
        d3.event.preventDefault();
        let projectId = d3.select('#project-id');
        let projectName = d3.select('#project-name');
        let description = d3.select('#description');
        let message = d3.select('#new-project-form > .form-message');

        if (projectId.node().validity.valueMissing) {
            message.classed('error', true);
            message.text('Please enter a project ID.');
            return;
        }
        if (projectId.node().validity.patternMismatch) {
            message.classed('error', true);
            message.text('The project ID can only contain lowercase letters, numbers, dot, dash, underscore, and can only start with a letter or number.');
            return;
        }
        if (projectName.node().validity.valueMissing) {
            message.classed('error', true);
            message.text('Please enter a project name.');
            return;
        }

        let project = {
            id: projectId.property('value'),
            name: projectName.property('value'),
            description: description.property('value') || null,
        };

        API_SERVICE.postProject(project)
        .then(response => {
            location.href = 'management.html';
        })
        .catch(error => {
            message.classed('error', true);
            if (error.response.status === 409) {
                message.text('The project ID already exists.');
                console.log(error.response.data);
            } else {
                message.text('An unknown problem occured.');
                console.error(error);
            }
        });
    });
});
