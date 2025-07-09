act-manual:
	curl \
	-X POST \
	-H 'Authorization: token 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' \
	-H "Accept: application/vnd.github.v3+json" \
	https://api.github.com/repos/DayBySay/study-githubactions/actions/workflows/manual.yml/dispatches \
	-d '{"ref":"main"}'

test:
	echo "test"
