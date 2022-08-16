# Blog Site

This is a dummy blog site, with a frontend, backend and database.

<p>
  <img width="330" height="335" src="https://imgs.xkcd.com/comics/blogging.png" alt="blogging">
</p>

Things this project _does not_ care about:
 - performance/scaling
 - security
 - UI

Things this project _does_ demonstrate:
 - poetry
 - Flask
 - Docker
 - Make
 - MySQL DB/migrations
 - separation of concerns
 - unit tests
 - coding style/checks

## Setup

This project requires Docker, NPM and Python. It also requires a `.env` file for `docker-compose` to work. To generate a `.env` in this directory do:

```shell
echo "MYSQL_HOST_PORT=3306" > .env
```

If you need to run the database on a different port you can just change the `.env` file contents, and check them with `docker-compose config`.

## Start

Use `docker-compose` to start up the site, via:

```
docker-compose up -d --build
```

You should see some output like:
> Creating db ... done
> Creating backend ... done
> Creating frontend ... done

Now the site is running locally and you can interact with it via your browser at [http://localhost:3000](localhost:3000).

## Data Backups

As you run and operate the site locally, you'll generate blog posts, comments, etc. If you destroy the database container you'll lose that data. In order to mitigate this, you can use a custom `flask` command on the `backend` Docker container to take a database snapshot and later restore from that snapshot.

First, ensure the site is running (see [Start](#start) above). Then access the `backend` container:

```
docker exec -it backend bash
```

Now you have a shell on the `backend` container and can use the `flask` CLI to manage the backups

### Create a backup

```
flask alchemydumps create
```

The above command will print output like the following:

> ==> 2 rows from Comments saved as /app/alchemydumps-backup/db-bkp-20220628204546-Comments.gz
>
> ==> 2 rows from Posts saved as /app/alchemydumps-backup/db-bkp-20220628204546-Posts.gz

That data is saved in the listed diretory, which is mounted locally to `backend/db-backups` so that you may destroy the `backend` container and not lose the snapshot. Check the `backend/db-backups` directory and you should see those same files listed:

```
ls -1 backend/db-backups
db-bkp-20220628204546-Comments.gz
db-bkp-20220628204546-Posts.gz
```

### Restore from backup

First, use the `history` command to find the revision IDs, there may be multiple if you've taken multiple backups previously.

```
flask alchemydumps history
```

The above command will print output like the following:

> ==> ID: 20220628204546 (from Jun 28, 2022 at 20:45:46)
>    /app/alchemydumps-backup/app/alchemydumps-backup/db-bkp-20220628204546-Comments.gz
>    /app/alchemydumps-backup/app/alchemydumps-backup/db-bkp-20220628204546-Posts.gz

Notice that `ID` above, we'll use that in the following command to restore from that snapshot:

```
flask alchemydumps restore -d 20220628204546
```

In the above example the ID `20220628204546` was used, but you'll substitute for whatever ID was listed in the `history` command. The restore command will print output like the following:

> ==> db-bkp-20220628204546-Comments.gz totally restored.
> ==> db-bkp-20220628204546-Posts.gz totally restored.

Now the database data has been replaced with the contents from the snapshot.

# TODO

0. user settings (just display date as an example, relative or absolute)
1. audit log/history
