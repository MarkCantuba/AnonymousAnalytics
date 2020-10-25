# Postman Guide

This folder contains all postman environments and API collections.

## Update Latest Postman Configurations

- Import project `postman` folder
    - If there are environments or collections that were previously imported, delete them first. Postman will create new environments and duplicate collections instead of updating the previous ones even if they share the same ids.

## Update Postman Configurations

- Make changes to environments
    - Press "Manage Environment" button with a "control panel" icon on the top right
    - Select an environment to update, or add a new environment
    - Compose an informative variable name, fill up the default value "initial value" field
        - Carefully think about the default value, it should make sense for everyone, or it should be empty if it depends on an API
        - Most variables should be present to make API usable under all envrionments, so feel free to make copies of them in all environments
- Make changes to APIs
    - Select an API request under a collection, or press "New" to create a new request
        - If an API makes better sense under another collection, feel free to move it
    - Select HTTP method for API, enter URLs and possibly add a body
    - Parameters in URL should be written as a variable defined in environments
        - This includes query parameters
        - For example, instead of `http://localhost:8080/api/v1/projects/noodlecake_sample/events?start=2020-10-11T07%3A00%3A00Z`, use `http://{{server_host}}/api/v1/projects/{{project_id}}?start={{start_utc}}`
        - Make sure to [encode URL reserved characters](https://en.wikipedia.org/wiki/Percent-encoding), most notably `:` (colon) in UTC time string, [free tool](https://meyerweb.com/eric/tools/dencoder/) everywhere from Google search
    - Use "Raw" and JSON for most request bodies
    - `ctrl-s`/`command-s` works, save before export!
- Export environments and APIs to project `postman` folder
    - Export each new or changed environment in "Manage Enviornment" dialog
        - Click "Download Environment" button
    - Export each collection with new or changed APIs
        - Right click on collection or left click on three dots
        - Click "Export"
        - Export as postman collection v2.1
    - As long as an update as documented above is performed after opening local development branch, override the files of old ones


## Use Postman

- Select an API
- Check if there are missing parameter values, change them at "Environment quick look"
- Press "Send"
- Inspect the response
    - Make sure to start local dev environment before using local environment configuration, otherwise `ECONNREFUSED` (connection refused) may occur

## Git Versioning

It is not required to sign up a postman account and share workspace as a team, but this means devs may not get the latest postman configuration when they develop new APIs, and when a merge request is created, there are likely conflicts on API changes.

In case a merge conflict is reported by git, dev should try to inspect the merge blocks to see what lines in the postman JSON are both modified.

For the latest postman version, the exported collection and environment has a field called `_postman_exported_at` with a UTC timestamp as a value. If there is a conflict on this line, **all below steps are relevant**.

- It is safe to ignore `id` field on top level that identifies an environment or a collection, as long as it is a UUID it should work.
- Pay attention to API blocks, usually it means a patch on master has added **another API** already. Choose "accept both changes" to prevent lose work from either side. **Make sure to check braces and commas**, they might be missing or at the wrong positions to form a valid JSON.
- If there is a "both modified" conflict on a specific field of API or environment, check with other devs or leads to discuss which one should be used.
