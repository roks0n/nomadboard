# nomadboard

### Starting a projects (same goes for dev)

1. Build the whole thing
`make build`

2. Run the whole thing
`make runserver`
TODO: gets below error, it gets fixed after a re-run, fix it so it works out of da box
`ERROR: Cannot start container f47ae0bf5b1b983ae36d5fc4d297084104587239da5f8637c53581cb3b35817c: Cannot link to a non running container: /nomad-postgres AS /nomad-web/nomad-db`

3. Apply migrations
`make migrate`

4. Create superuser
`make superuser`

### Development
4. If you do any changes to models, you must create migrations
`make migrations`
