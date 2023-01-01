# Soulstone

Soulstone - a electronic record system for spiritual healers

## CLI Commands

`flask commands db_create` creates the database
`flask commands db_seed` inserts test practices and users
`flask commands db_drop` drops the database

## Useful make commands (Requires buildtools and docker/docker-compose)

### Install make

- [Windows](https://gnuwin32.sourceforge.net/packages/make.htm#:~:text=Make%20is%20a%20tool%20which,compute%20it%20from%20other%20files.)
- [MacOS](https://www.freecodecamp.org/news/how-to-download-and-install-xcode/)
- [Linux](https://wiki.gnucash.org/wiki/Install_Build_Tools)

### Useful Make commands

> Note: See ./Makefile for full list`

- `make up` - Start compose, create the initial database without seeds
- `make stop` - Stop a current instance without effecting the DB (needs to be created first)
- `make start` - Start a stopped instance
- `make test_env` - Start a fresh instance with test data WARNING: WILL DELETE EXISTING STUFF
- `make logs` - Show logs from running containers
- `make login-soulstone` - Login to the soulstone container for tomfoolery and shenanigans
