# nomadboard

### Starting a projects (in development & production)
1. Build everything
`make bootstrap`
`make migrate`

2. Create superuser
`make superuser`

3. Run the whole thing
`make runserver`

### Development
1. If you do any changes to models, you must create migrations
`make migrations`

2. After running `make migrations` you have to apply those migrations
`make migrate`

### Updating Scrapers and running spiders
1. Sync all the spiders with the database
`DJANGO_CMD=sync_spiders make django`
2. Run a spider
`DJANGO_CMD="run_spider --scraper_slug <scraper-slug-here>" make django`

### Production
1. Run server in production
`make run-production`

2. Start Scheduler
`nohup make django DJANGO_CMD='process_xml --source_id="1,2" >> scheduler.log`

