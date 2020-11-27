'use strict';

class APIService {
    constructor(env) {
        switch (env) {
            case 'DEV':
                this.$axios = axios.create({
                    baseURL: 'http://localhost:8080'
                });
                break;
            case 'INTEGRATION':
                this.$axios = axios.create({
                    baseURL: 'http://138.197.161.129/api/v1'
                });
                break;
            default:
                this.$axios = axios.create({
                    baseURL: '/api/v1'
                });
                break;
        }
    }

    postProject(project) {
        return this.$axios.post('/projects', project);
    }

    getProjects() {
        return this.$axios.get('/projects');
    }

    getProject(projectId) {
        return this.$axios.get(`/projects/${projectId}`);
    }

    getEventCounts(projectId, start, end, interval) {
        return this.$axios.get(`/projects/${projectId}/events/counts`, {
            params: {
                start: start.toISO(),
                end: end.toISO(),
                interval: interval
            }
        });
    }
}

const API_SERVICE = new APIService();
