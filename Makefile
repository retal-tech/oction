ifneq (,$(wildcard ./.env))
	env_exist = 1
    include .env
    export
else
	env_exist = 0
endif

_check:
ifneq ($(env_exist), 1)
	 @(echo "\n\n\tNo env file \n\tTry cp .env.ex .env\n\n"; exit 1)
endif

dev:_check
	@echo Make sure you set DEBUG=1 in .env
	@docker-compose -f docker-compose.dev.yml up
	@echo exposed on http://0.0.0.0:$(NGINX_EXPOSE)

prod:
	@echo Make sure you set DEBUG=0 in .env
	@docker-compose -f docker-compose.prod.yml up
