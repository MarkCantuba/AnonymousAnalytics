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

    getProjcets() {
        return this.$axios.get('/projects');
    }

    getEvents(projectName, start, end) {
        return this.$axios.get(`/projects/${projectName}/events`, {
            start: start,
            end: end
        });
    }
}

const API_SERVICE = new APIService();
