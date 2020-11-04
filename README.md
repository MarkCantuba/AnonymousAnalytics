# Anonymous Analytics

Anonymous Analytics is an analytics service targeting game developers to collect and analyze data with their own choices. Unlike existing analytics services on the market that automatically collecting user privacy data, developers have full control over which data to be sent and stored in Anonymous Analytics.

**[Checkout our demo here!](http://138.197.161.129/)**

## Features

- A web service with a set of well-defined REST APIs to send and store data
- An evolving user-friendly webpage to show aggregated data by charts
- A management portal to organize data under different projects.
- Self-hosting or cloud-hosting web service in minutes

The team also plans to support client SDKs that can be integrated into mainstream game engines.

## Project Wiki

The [project wiki](https://git.cs.usask.ca/CMPT371-01-2020/anonymous-analytics/-/wikis/home) includes our general guidelines, management documentations, and more. The team plans to organize user documentation as well.

## Issues

Report issues and check our progress [here](https://git.cs.usask.ca/CMPT371-01-2020/anonymous-analytics/-/issues). Our maintainers will verify and arrange issues based on team priority and schedules.

## Contributing

Just clone the repo, and check out development guides in code repository.

- [Backend development guide](src/README.md) introduces how to setup a local backend API server with datastore.
- [Frontend development guide](static/README.md) introduces how to setup local frontend with backend on various available environments.
- [Server provisioning guide](ansible/README.md) is a starting point to spin up servers and dependencies on a cloud hosted or self hosted environment.
- [Postman guide](postman/README.md) descrbies a standardized way to verify backend APIs in postman.

For a full local environment, backend development guide + frontend development guide is a good start. For a light-weight, frontend only environment, frontend development guide also provides an option to use demo servers as data source for visualizations. For hosting a separate environment, checkout server provisioning guide.

There is also a [development FAQ](https://git.cs.usask.ca/CMPT371-01-2020/anonymous-analytics/-/wikis/Documentations/FAQ) pages in project wiki.

## References

For more information about tech stacks, we use [FastAPI](https://fastapi.tiangolo.com/) for backend server, [Elasticsearch](https://www.elastic.co/elasticsearch/) as our datastore, [c3.js](https://c3js.org/) over [d3.js](https://d3js.org/) for our frontend visualization, [ansible](https://www.ansible.com/) for automated server provisioning, and the demo service is hosted on [DitigalOcean](https://www.digitalocean.com/).
