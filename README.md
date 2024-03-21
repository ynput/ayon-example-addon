Example addon
=============

* New directory structure - the good one *


Premises
--------

Addon repository (at least its server part) should work when cloned in the addon directory.

```bash
cd addons/
mkdir example
cd example
git clone https://github.com/ynput/ayon-example-rez-addon dev
```


Value of the version part of the addon path is not significant, so for development, it is possible to use `dev`.

```
addons/example
  ├── 1.0.0
  └── dev
      ├── client
      ├── frontend
      │   ├── dist
      │   └── package.json
      ├── package
      ├── package.py
      ├── private
      ├── public
      ├── README.md
      ├── server
      │   ├── __init__.py
      │   ├── settings.py
      │   └── site_settings.py
      └── services
```

Name of the addon and its version is defined in `package.py` it is the single source of truth for the version information.

The addon build script (implementation TBD - rez build?) creates a zip package with similar structure as the repository itself,
but should ommit files not needed by the server and buil


Directory structure
-------------------

### client

Source code of the client code. Build script (?) should create a client zip file from the source and put it to `private` directory,
create `checksums.json` and include it to the zip file. **TODO**

### frontend

Web frontend of the addon. Frontend is served if `frontend/dist/index.html` exists.
If the frontend is a javascript app, dist directory should be gitignored, build script should run `yarn build` (or equivalent)
and put the `frontend/dist` to the resulting zip package. 

Other files (`src/`, `package.json`, `node_modules`...) should not be packed.

Frontend is no longer a subdirectory of "server".

### package

Target directory where the build script should put the resulting zip file as `{addon_name}-{addon_version}.zip`

This directory should be gitignored.

### private

Contains static content available for download for authenticated users.

If the addon does not use this functionality, the directory shouldn't be present.
If the directory exists, build script packs it to the resulting zip file.

### public

Contains static content available for download publicly.

If the addon does not use this functionality, the directory shouldn't be present.
If the directory exists, build script packs it to the resulting zip file.

### server

Python server-side part of the addon. Contains an implementation of `BaseServerAddon` class.

### services

This directory shouldn't be present in the resulting zip file.


### package.py

This file MUST be present in the resulting zip file
