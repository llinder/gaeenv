.PHONY: deploy deploy-github deploy-pypi update-pypi clean tests

deploy-github:
	git tag `grep "gaeenv_version =" gaeenv.py | grep -o -E '[0-9]\.[0-9]\.[0-9]{1,2}'`
	git push --tags origin master

deploy-pypi:
	python setup.py sdist upload

update-pypi:
	python setup.py register

deploy: deploy-github deploy-pypi

clean:
	@rm -rf gaeenv.egg-info/
	@rm -rf dist/
	@rm -rf build/
	@rm -rf env/

test1:
	@echo " * test1: list versions and install latest"
	@rm -rf env                           && \
		virtualenv --no-site-packages env && \
		. env/bin/activate                && \
        pip install requests              && \
		python setup.py install           && \
		gaeenv -vv list sdk               && \
                gaeenv -vv install sdk

tests: clean test1
