# Make your secrets...

Copy `openshift/example-secrets.yaml`, edit to make some other passwords, remove '-example' from the
`metadata.name`

# Apply the manifests

This should create all the relevant deployments, services, etc.

```bash
oc apply -f openshift/
```

Then wait a bit for things to builds to finish and containers to start...

# TODO: setup routes to expose externally
# TODO: setup ssl

# Initialize database

```bash
oc rsh -c hypis-worker deploy/hypis bin/hypothesis init
oc rsh -c hypis-worker deploy/hypis bin/hypothesis migrate upgrade head
```

# Setup an admin user

Following instructions from
"[Accessing the admin interface](https://h.readthedocs.io/en/latest/developing/administration/)".

This will prompt for a name, email address and password. TODO: script this better, or make a
"devdata" equivalent to what the upstream developers do.

```bash
oc rsh -c hypis-worker deploy/hypis bin/hypothesis user add
```

```bash
oc rsh -c hypis-worker deploy/hypis bin/hypothesis user admin ${USERNAME}
```

# Other TODOs

- tune memory
- scale elasticsearch?
- disable newrelic?
