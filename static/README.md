# Frontend Development Guide

This directory contain all source code for frontend development.

## Frontend Environment Setup

Overall, python 3 and a modern browser are required.
- [Chrome](https://www.google.com/intl/en_ca/chrome/) and [Firefox](https://www.mozilla.org/en-CA/firefox/new/) are good browser candidates. Do install and test both if possible.
- Chromium based Edge on Windows and Safari on macOS should be supported too, but it is not required to make the app displayed as perfect as in Chrome and Firefox.
- Mobile browsers and designs are not required at this time.

An optional backend setup would be beneficial but not necessary. All development can be done by using data and API from integration enviornment.

## Test Frontend Webpage

- Navigate to `<project_root>/util/static_helper`
- Run `python static_helper.py`
- In browser, go to `http://localhost/welcome.html`
    - It should display project home page, currently with "Hello CMPT 371 Anonymous Analytics!" and a link to project detail page
- Do any changes in files under `<project_root>/static` directory
    - For example, change the text in `<h1>` tag in `welcome.html` to `Hello World!`.
- Refresh browser page, the changes should now be reflected

## Changing Environments

Usually, the dataset on integration environment should be more comprehensive to visualize than that in local environment. Frontend visualization should be tested with integration dataset to better reflect what clients would see.

- To test with a specific environment, add an environment string to the `APIService` instance
    - Change `const API_SERVICE = new APIService();` on the last line to `const API_SERVICE = new APIService('INTEGRATION'); // or 'DEV'`
        - `DEV` is optional, but if used, local backend is required
        - Reference to backend development guide under `<project_root>/src` to setup a backend
    - **Make sure to revert this change before any commit to git**, so it won't mess up integration frontend
- In browser, go to `http://localhost/welcome.html`, and then click on the link
    - If API request succeeds, there should be a bar graph showing some dummy data
    - Or else error should be logged on console
        - Press F12 open developer tools and inspect console

## Future Goals

- Compress files
- Explore options with ES6 Modules
